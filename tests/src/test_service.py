# Jormungandr
from func.src.services.post_user_ticket import CreateTicketService
from .stubs import StubAttachmentUploadInstance, StubUser, StubGetUsers, stub_user_mongo

# Standards
from unittest.mock import patch

# Third party
from zenpy.lib.api_objects import User


@patch.object(CreateTicketService, '_get_zenpy_client')
def test_get_or_create_user(mock_zenpy_client, client_create_ticket_service):
    mock_zenpy_client().users.return_value = StubGetUsers().append_user(StubUser(external_id=102030))
    user = client_create_ticket_service._get_or_create_user()

    assert isinstance(user, StubUser)
    assert user.external_id == client_create_ticket_service.jwt_decoded['user']['unique_id']


@patch('func.src.service.CreateTicketService.user_repository.find_user_by_unique_id', return_value=stub_user_mongo)
@patch.object(CreateTicketService, "_get_zenpy_client")
def test_get_or_create_user_if_user_not_exists(mock_zenpy_client, mock_repository_find_one, client_create_ticket_service):
    mock_zenpy_client().users.return_value = None
    mock_zenpy_client().users.create.return_value = User(name='teste', email='email', external_id=102030)
    user = client_create_ticket_service._get_or_create_user()

    assert user.name == 'teste'
    assert user.email == 'email'
    assert user.external_id == 102030


@patch.object(CreateTicketService, '_get_zenpy_client')
def test_get_or_create_user_if_zenpy_client_was_called(mock_zenpy_client, client_create_ticket_service):
    client_create_ticket_service._get_or_create_user()

    mock_zenpy_client.assert_called_once_with()


@patch.object(CreateTicketService, '_get_zenpy_client')
def test_get_or_create_user_if_zenpy_client_users_was_called(mock_zenpy_client, client_create_ticket_service):
    client_create_ticket_service._get_or_create_user()

    mock_zenpy_client().users.assert_called_once_with(external_id=102030)


@patch('func.src.service.CreateTicketService.user_repository.find_user_by_unique_id', return_value=stub_user_mongo)
@patch.object(CreateTicketService, "_get_zenpy_client")
def test_get_or_create_user_not_exists_if_mongo_find_user_by_unique_id_was_called(mock_zenpy_client, mock_mongo_find_one, client_create_ticket_service):
    mock_zenpy_client().users.return_value = False
    client_create_ticket_service._get_or_create_user()

    mock_mongo_find_one.assert_called_once_with(unique_id=102030)


@patch('func.src.service.CreateTicketService.user_repository.find_user_by_unique_id', return_value=stub_user_mongo)
@patch.object(CreateTicketService, "_get_zenpy_client")
def test_get_or_create_user_not_exists_if_client_users_create_was_called(mock_zenpy_client, mock_mongo_find_one, client_create_ticket_service):
    mock_zenpy_client().users.return_value = False
    client_create_ticket_service._get_or_create_user()

    mock_zenpy_client().users.create.assert_called_once()


@patch.object(CreateTicketService, "_get_zenpy_client")
def test_when_have_attachments_then_return_attachments_tokens(mock_zenpy_client, client_create_ticket_service_with_attach):
    mock_zenpy_client().attachments.upload.return_value = StubAttachmentUploadInstance(token=10)
    attachment_tokens = client_create_ticket_service_with_attach._get_attachments()

    assert isinstance(attachment_tokens, list)
    assert attachment_tokens[0] == 10


@patch.object(CreateTicketService, "_get_zenpy_client")
def test_get_attachments_if_zenpy_client_was_called(mock_zenpy_client, client_create_ticket_service_with_attach):
    client_create_ticket_service_with_attach._get_attachments()

    mock_zenpy_client.assert_called_once_with()


@patch.object(CreateTicketService, "_get_zenpy_client")
def test_get_attachments_if_zenpy_client_attachments_was_called(mock_zenpy_client, client_create_ticket_service_with_attach):
    client_create_ticket_service_with_attach._get_attachments()

    mock_zenpy_client().attachments.upload.assert_called_once()


@patch.object(CreateTicketService, "_get_zenpy_client")
def test_when_attachments_is_empty_then_return_empty_list(mock_zenpy_client, client_create_ticket_service):
    attachment_tokens = client_create_ticket_service._get_attachments()

    assert attachment_tokens == []


@patch.object(CreateTicketService, "_get_zenpy_client")
def test_get_attachments_if_raises_zenpy_client_was_not_called(mock_zenpy_client, client_create_ticket_service):
    client_create_ticket_service._get_attachments()

    mock_zenpy_client.assert_not_called()


@patch.object(CreateTicketService, '_get_zenpy_client')
@patch.object(CreateTicketService, '_get_or_create_user', return_value=StubUser(id=10))
def test_set_tickets(mock_get_or_create_user, mock_zenpy_client, client_create_ticket_service):
    response = client_create_ticket_service.set_tickets()

    assert response is True


@patch.object(CreateTicketService, '_get_zenpy_client')
@patch.object(CreateTicketService, '_get_or_create_user', return_value=StubUser(id=10))
def test_set_tickets_if_zenpy_client_was_called(mock_get_or_create_user, mock_zenpy_client, client_create_ticket_service):
    client_create_ticket_service.set_tickets()

    mock_zenpy_client.assert_called_once_with()


@patch.object(CreateTicketService, '_get_zenpy_client')
@patch.object(CreateTicketService, '_get_or_create_user', return_value=StubUser(id=10))
def test_set_tickets_if_zenpy_client_tickets_create_was_called(mock_get_or_create_user, mock_zenpy_client, client_create_ticket_service):
    client_create_ticket_service.set_tickets()

    mock_zenpy_client().tickets.create.assert_called_once()


@patch.object(CreateTicketService, '_get_zenpy_client')
@patch.object(CreateTicketService, '_get_or_create_user', return_value=StubUser(id=10))
def test_set_tickets_if_get_or_create_user_was_called(mock_get_or_create_user, mock_zenpy_client, client_create_ticket_service):
    client_create_ticket_service.set_tickets()

    mock_get_or_create_user.assert_called_once_with()
