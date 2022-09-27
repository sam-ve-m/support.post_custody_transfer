import pytest
from etria_logger import Gladsheim
from unittest.mock import MagicMock, patch
from src.domain.exceptions.exceptions import ErrorWithZendesk
from src.repository.zendesk.repository import ZendeskRepository
from zenpy.lib.api_objects import User, Ticket, Comment, CustomField

fake_zenpy_client = MagicMock()
fake_infra = MagicMock()
fake_infra.get_connection.return_value = fake_zenpy_client

dummy_name = "name"
dummy_token = "token"
dummy_temp_file = "temp_file"
fake_zenpy_client.attachments.upload.return_value.token = dummy_token


def test_upload_file(monkeypatch):
    monkeypatch.setattr(ZendeskRepository, "infra", fake_infra)
    response = ZendeskRepository._upload_file(dummy_temp_file, dummy_name)
    fake_zenpy_client.attachments.upload.assert_called_once_with(fp=dummy_temp_file, target_name=dummy_name)
    assert response == dummy_token


dummy_unique_id = "asdansdij12j3n1orno3f204102fj1031r"
dummy_user = "user"


def test_get_user(monkeypatch):
    fake_zenpy_client.users.return_value.values = [dummy_user, None]
    monkeypatch.setattr(ZendeskRepository, "infra", fake_infra)
    response = ZendeskRepository.get_user(dummy_unique_id)
    assert response == dummy_user


def test_get_user_no_user(monkeypatch):
    fake_zenpy_client.users.return_value = None
    monkeypatch.setattr(ZendeskRepository, "infra", fake_infra)
    response = ZendeskRepository.get_user(dummy_unique_id)
    assert response is None


dummy_user_data = MagicMock(nick_name=True, email=True, unique_id=True)


@patch.object(User, "__init__", return_value=None)
def test_create_user(mocked_user, monkeypatch):
    fake_zenpy_client.users.create.return_value = dummy_user
    monkeypatch.setattr(ZendeskRepository, "infra", fake_infra)
    response = ZendeskRepository.create_user(dummy_user_data)
    assert response == dummy_user


dummy_exception = ErrorWithZendesk()
expected_create_exception_message = "Jormungandr::CreateTicketService::create_user::Failed to create user"


@patch.object(Gladsheim, "error")
@patch.object(User, "__init__", return_value=None)
def test_create_user_with_errors(mocked_user, mocked_logger, monkeypatch):
    fake_zenpy_client.users.create.side_effect = dummy_exception
    monkeypatch.setattr(ZendeskRepository, "infra", fake_infra)
    with pytest.raises(ErrorWithZendesk):
        ZendeskRepository.create_user(dummy_user_data)
    mocked_logger.assert_called_once_with(error=dummy_exception, message=expected_create_exception_message)


dummy_snapshot = "First"
dummy_attachments = []
stub_user = MagicMock(id=dummy_user)


@patch.object(Comment, "__init__", return_value=None)
def test_set_comment(mocked_comment):
    ZendeskRepository.set_comment(stub_user, dummy_snapshot, dummy_attachments)
    mocked_comment.assert_called_once_with(
        author_id=dummy_user,
        html_body=dummy_snapshot,
        uploads=dummy_attachments,
        public=False,
    )


dummy_id = "id"
dummy_value = "value"


dummy_method = "method"
dummy_subject = "subject"
dummy_comment = "comment"
dummy_ticket_type = "ticket_type"


@patch.object(Ticket, "__init__", return_value=None)
def test_set_ticket(mocked_ticket, monkeypatch):
    monkeypatch.setattr(ZendeskRepository, "method", dummy_method)
    ZendeskRepository.set_ticket(
        dummy_subject, stub_user, dummy_ticket_type, dummy_comment
    )
    mocked_ticket.assert_called_once_with(
        subject=dummy_subject,
        requester_id=dummy_user,
        ticket_type=dummy_ticket_type,
        via=dummy_method,
        comment=dummy_comment,
    )


dummy_ticket = MagicMock()


def test_post_ticket(monkeypatch):
    fake_zenpy_client.tickets.create.return_value = dummy_user
    monkeypatch.setattr(ZendeskRepository, "infra", fake_infra)
    response = ZendeskRepository.post_ticket(dummy_ticket)
    assert response == dummy_user


expected_post_ticket_exception_message = "Jormungandr::CreateTicketService::set_tickets::Failed to create ticket"


@patch.object(Gladsheim, "error")
def test_post_ticket_with_errors(mocked_logger, monkeypatch):
    fake_zenpy_client.tickets.create.side_effect = dummy_exception
    monkeypatch.setattr(ZendeskRepository, "infra", fake_infra)
    with pytest.raises(dummy_exception.__class__):
        ZendeskRepository.post_ticket(dummy_ticket)
    mocked_logger.assert_called_once_with(error=dummy_exception, message=expected_post_ticket_exception_message)

