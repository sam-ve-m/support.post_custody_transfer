# Standards

# Third part
from zenpy.lib.api_objects import User

# Jormungandr
from ..domain.validator import TicketValidator
from ..repository.user.repository import UserRepository
from ..repository.zendesk.repository import ZendeskRepository


class CreateTicketService:
    zendesk_repository = ZendeskRepository
    user_repository = UserRepository

    @classmethod
    def set_tickets(cls, snapshot: str, params: TicketValidator, decoded_jwt: dict) -> bool:
        unique_id = decoded_jwt["user"]["unique_id"]
        user = cls._get_or_create_user(unique_id)
        attachments_token = [
            cls.zendesk_repository.set_attachment(attachment)
            for attachment in params.attachments
        ]
        comment = cls.zendesk_repository.set_comment(user, snapshot, attachments_token)
        ticket = cls.zendesk_repository.set_ticket(user, comment)
        return cls.zendesk_repository.post_ticket(ticket)

    @classmethod
    def _get_or_create_user(cls, unique_id: str) -> User:
        if not (user := cls.zendesk_repository.get_user(unique_id)):
            if user_data := cls.user_repository.find_user_by_unique_id(unique_id=unique_id):
                user = cls.zendesk_repository.create_user(user_data)
            else:
                raise ValueError("Unable to find user")
        return user
