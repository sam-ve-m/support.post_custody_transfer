# Jormungandr
from func.src.domain.validator import TicketValidator
from func.src.services.post_user_ticket import CreateTicketService
from tests.src.img import attachment1

# Standards
from unittest.mock import patch

# Third party
from pytest import fixture

jwt_test = {"user": {"unique_id": 102030}}
params_test = {"subject": 'assunto', "description": "descrição do ticket", "attachments": [], 'ticket_type': 'problem'}


@fixture(scope="function")
def client_create_ticket_service():
    client_create_ticket_service = CreateTicketService(
        x_thebes_answer=jwt_test,
        params=TicketValidator(**params_test),
        url_path="",
    )
    return client_create_ticket_service


@fixture(scope="function")
def client_create_ticket_service_with_attach():
    client_create_ticket_service = CreateTicketService(
        x_thebes_answer=jwt_test,
        params=TicketValidator(**params_test),
        url_path="",
    )
    client_create_ticket_service.params["attachments"].append(attachment1)
    return client_create_ticket_service
