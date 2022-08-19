# Standards

# Third part
from zenpy.lib.api_objects import User

from ...domain.enums.enums import TicketType
# Jormungandr
from ...domain.models.request.model import TicketValidator
from ...repository.user.repository import UserRepository
from ...repository.zendesk.repository import ZendeskRepository
from ...transport.jormungadr.transport import JormungandrTransport


class CreateTicketService:
    jormungandr_transport = JormungandrTransport
    zendesk_repository = ZendeskRepository
    user_repository = UserRepository
    SUBJECT = "Transferência de Custódia"
    TICKET_TYPE: str = TicketType.PROBLEM.value
    DESCRIPTION = "Eu gostaria de realizar uma transferência de custódia para outra corretora."

    @classmethod
    def set_tickets(cls, snapshot: str, params: TicketValidator, decoded_jwt: dict, jwt: str) -> bool:
        unique_id = decoded_jwt["user"]["unique_id"]
        user = cls._get_or_create_user(unique_id)
        attachments_token = [
            cls.zendesk_repository.set_attachment(attachment)
            for attachment in params.attachments
        ]
        comment = cls.zendesk_repository.set_comment(user, snapshot, attachments_token)
        ticket = cls.zendesk_repository.set_ticket(cls.SUBJECT, user, cls.TICKET_TYPE, comment)
        open_ticket = cls.zendesk_repository.post_ticket(ticket)
        return cls.jormungandr_transport.update_ticket_with_comment(jwt, open_ticket.ticket.id, cls.DESCRIPTION)

    @classmethod
    def _get_or_create_user(cls, unique_id: str) -> User:
        if not (user := cls.zendesk_repository.get_user(unique_id)):
            if not (user_data := cls.user_repository.find_user_by_unique_id(unique_id=unique_id)):
                raise ValueError("Unable to find user")
            user = cls.zendesk_repository.create_user(user_data)
        return user
