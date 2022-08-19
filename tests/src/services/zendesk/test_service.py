# Third part
import pytest
from unittest.mock import MagicMock, patch

# Jormungandr
from src.services.zendesk.service import CreateTicketService


fake_zendesk_repository = MagicMock()
fake_jormungandr_transport = MagicMock()

dummy_unique_id = "id"
dummy_decoded_jwt = {"user": {"unique_id": dummy_unique_id}}
dummy_jwt = "jwt"


dummy_attachments = None
stub_attachments = [dummy_attachments]

dummy_user = "user"
dummy_snapshot = "snapshot"

dummy_custom_fields = "custom_fields"

dummy_ticket_type = "ticket_type"
dummy_comment = "comments"
dummy_subject = "subject"
dummy_description = "description"

dummy_ticket = "ticket"

dummy_params = MagicMock(
    attachments=stub_attachments,
    custom_fields=dummy_custom_fields,
    subject=dummy_subject,
    description=dummy_description,
    ticket_type=dummy_ticket_type,
)
stub_open_ticket_id = 1515


@patch.object(CreateTicketService, "_get_or_create_user", return_value=dummy_user)
def test_set_tickets(mocked_get_user, monkeypatch):
    fake_zendesk_repository.set_attachment.return_value = dummy_attachments
    fake_zendesk_repository.set_comment.return_value = dummy_comment
    fake_zendesk_repository.set_ticket.return_value = dummy_ticket
    fake_zendesk_repository.post_ticket.return_value.ticket.id = stub_open_ticket_id
    fake_jormungandr_transport.update_ticket_with_comment.return_value = True

    monkeypatch.setattr(CreateTicketService, "zendesk_repository", fake_zendesk_repository)
    monkeypatch.setattr(CreateTicketService, "jormungandr_transport", fake_jormungandr_transport)
    monkeypatch.setattr(CreateTicketService, "SUBJECT", dummy_subject)
    monkeypatch.setattr(CreateTicketService, "DESCRIPTION", dummy_description)
    monkeypatch.setattr(CreateTicketService, "TICKET_TYPE", dummy_ticket_type)
    response = CreateTicketService.set_tickets(dummy_snapshot, dummy_params, dummy_decoded_jwt, dummy_jwt)
    mocked_get_user.assert_called_once_with(dummy_unique_id)
    assert response is True

    fake_zendesk_repository.set_attachment.assert_called_once_with(dummy_attachments)
    fake_zendesk_repository.set_comment.assert_called_once_with(dummy_user, dummy_snapshot, stub_attachments)
    fake_zendesk_repository.set_ticket.assert_called_once_with(
        dummy_subject, dummy_user, dummy_ticket_type, dummy_comment
    )
    fake_zendesk_repository.post_ticket.assert_called_once_with(dummy_ticket)
    fake_jormungandr_transport.update_ticket_with_comment.assert_called_once_with(
        dummy_jwt, stub_open_ticket_id, dummy_description)


fake_user_repository = MagicMock()


def test_get_or_create_user_getting(monkeypatch):
    fake_zendesk_repository.get_user.return_value = dummy_user
    monkeypatch.setattr(CreateTicketService, "user_repository", fake_user_repository)
    monkeypatch.setattr(CreateTicketService, "zendesk_repository", fake_zendesk_repository)
    response = CreateTicketService._get_or_create_user(dummy_unique_id)
    fake_zendesk_repository.get_user.assert_called_with(dummy_unique_id)
    fake_user_repository.find_user_by_unique_id.assert_not_called()
    fake_zendesk_repository.create_user.assert_not_called()
    assert response == dummy_user


def test_get_or_create_user_missing(monkeypatch):
    fake_zendesk_repository.get_user.return_value = False
    fake_user_repository.find_user_by_unique_id.return_value = False
    monkeypatch.setattr(CreateTicketService, "user_repository", fake_user_repository)
    monkeypatch.setattr(CreateTicketService, "zendesk_repository", fake_zendesk_repository)
    with pytest.raises(ValueError):
        CreateTicketService._get_or_create_user(dummy_unique_id)
    fake_zendesk_repository.get_user.assert_called_with(dummy_unique_id)
    fake_user_repository.find_user_by_unique_id.assert_called_with(unique_id=dummy_unique_id)
    fake_zendesk_repository.create_user.assert_not_called()


dummy_user_data = "user_data"


def test_get_or_create_user_creating(monkeypatch):
    fake_zendesk_repository.get_user.return_value = False
    fake_user_repository.find_user_by_unique_id.return_value = dummy_user_data
    fake_zendesk_repository.create_user.return_value = dummy_user
    monkeypatch.setattr(CreateTicketService, "user_repository", fake_user_repository)
    monkeypatch.setattr(CreateTicketService, "zendesk_repository", fake_zendesk_repository)
    response = CreateTicketService._get_or_create_user(dummy_unique_id)
    fake_zendesk_repository.get_user.assert_called_with(dummy_unique_id)
    fake_user_repository.find_user_by_unique_id.assert_called_with(unique_id=dummy_unique_id)
    fake_zendesk_repository.create_user.assert_called_with(dummy_user_data)
    assert response == dummy_user
