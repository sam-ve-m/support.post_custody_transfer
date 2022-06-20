# Standards
from base64 import b64decode
from os import SEEK_SET
from tempfile import TemporaryFile
from typing import List

# Third part
from decouple import config
from etria_logger import Gladsheim
from nidavellir import Sindri
from pydantic import BaseModel
from zenpy import Zenpy
from zenpy.lib.api_objects import User, Ticket, Via, Comment, Attachment, CustomField

# Jormungandr
from ..domain.enums import TicketType
from ..repository.snapshot.repository import SnapshotRepository
from ..repository.user.repository import UserRepository


class CreateTicketOfCustodyTransferService:
    zenpy_client = None
    user_repository = UserRepository
    snapshot_repository = SnapshotRepository

    SUBJECT = "Transferência de Custódia"
    FILE_NAME = "stvm.pdf"

    @classmethod
    def _get_zenpy_client(cls):
        if cls.zenpy_client is None:
            try:
                cls.zenpy_client = Zenpy(
                    email=config("ZENDESK_EMAIL"),
                    password=config("ZENDESK_PASSWORD"),
                    subdomain=config("ZENDESK_SUBDOMAIN"),
                )
            except Exception as ex:
                message = "_get_zenpy_client::error to get Zenpy Client"
                Gladsheim.error(error=ex, message=message)
                raise ex
        return cls.zenpy_client

    def __init__(self, jwt: str, params: BaseModel, decoded_jwt: dict):
        self.decoded_jwt = decoded_jwt
        self.params = params.dict()
        self.jwt = jwt
        Sindri.dict_to_primitive_types(self.params),

    def _get_attachments(self) -> List[Attachment]:
        attachment_tokens = list()
        file_bytes = b64decode(self.params["stvm"])
        with TemporaryFile() as temp_file:
            temp_file.write(file_bytes)
            temp_file.seek(SEEK_SET)
            zenpy_client = self._get_zenpy_client()
            upload_instance = zenpy_client.attachments.upload(
                fp=temp_file, target_name=self.FILE_NAME
            )
            attachment_tokens.append(upload_instance.token)
        return attachment_tokens

    def _get_or_create_user(self, unique_id: str) -> User:
        zenpy_client = self._get_zenpy_client()
        if user_results := zenpy_client.users(external_id=unique_id):
            user_zenpy = user_results.values[0]
            return user_zenpy
        user_created = self._create_user(unique_id)
        return user_created

    def _create_user(self, unique_id: str):
        if not (user_data := self.user_repository.find_user_by_unique_id(unique_id=unique_id)):
            raise ValueError("Unable to find user")
        user_obj = User(
            name=user_data["nick_name"], email=user_data["email"], external_id=user_data["unique_id"]
        )
        zenpy_client = self._get_zenpy_client()
        try:
            user_obj = zenpy_client.users.create(user_obj)
            return user_obj
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message=f"Jormungandr::CreateTicketService::create_user::Failed to create user",
            )
            raise ex

    def set_tickets(self):
        unique_id = self.decoded_jwt["user"]["unique_id"]
        user = self._get_or_create_user(unique_id)
        attachments_token = self._get_attachments()
        snapshot = self.snapshot_repository.snapshot_user_data(self.jwt)
        comment = Comment(
            author_id=user.id,
            html_body=snapshot,
            uploads=attachments_token,
            public=False,
        )
        ticket = Ticket(
            subject=self.SUBJECT,
            requester_id=user.id,
            ticket_type=TicketType.PROBLEM,
            via=Via(source="api"),
            comment=comment,
        )

        zenpy_client = self._get_zenpy_client()
        try:
            zenpy_client.tickets.create(ticket)
            return True
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message=f"Jormungandr::CreateTicketService::set_tickets::Failed to create ticket",
            )
            raise ex
