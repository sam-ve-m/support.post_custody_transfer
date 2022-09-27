from http import HTTPStatus

import pytest
import requests
from decouple import AutoConfig

from unittest.mock import patch, MagicMock

from src.transport.jormungadr.transport import JormungandrTransport
from src.domain.exceptions.exceptions import JormungandrCommunication
from src.domain.models.snapshot.model import Snapshot

fake_response = MagicMock()
dummy_response = {"response": True}
stub_response = {"result": dummy_response}
dummy_jwt = "15919as5da95s1azsx591a9s51dfa"
dummy_ticket_id = 151515947
dummy_comment = "Comment"


@patch.object(requests, "get", return_value=fake_response)
@patch.object(AutoConfig, "__call__", return_value=None)
@patch.object(Snapshot, "build")
def test_request_snapshot(mocked_snapshot, mocked_env, mocked_requests):
    fake_response.status_code = HTTPStatus.OK
    fake_response.json.return_value = stub_response
    JormungandrTransport.request_snapshot(dummy_jwt)
    mocked_requests.assert_called_once_with(None, headers={"x-thebes-answer": dummy_jwt})


@patch.object(requests, "get", return_value=fake_response)
@patch.object(AutoConfig, "__call__", return_value=None)
@patch.object(Snapshot, "build")
def test_request_snapshot_bad_status(mocked_snapshot, mocked_env, mocked_requests):
    fake_response.status_code = HTTPStatus.BAD_REQUEST
    with pytest.raises(JormungandrCommunication):
        JormungandrTransport.request_snapshot(dummy_jwt)
    mocked_requests.assert_called_once_with(None, headers={"x-thebes-answer": dummy_jwt})
    mocked_snapshot.assert_not_called()


@patch.object(requests, "get", side_effect=Exception())
@patch.object(AutoConfig, "__call__", return_value=None)
@patch.object(Snapshot, "build")
def test_request_snapshot_impossible_to_reach_url(mocked_snapshot, mocked_env, mocked_requests):
    with pytest.raises(JormungandrCommunication):
        JormungandrTransport.request_snapshot(dummy_jwt)
    mocked_requests.assert_called_once_with(None, headers={"x-thebes-answer": dummy_jwt})
    mocked_snapshot.assert_not_called()


@patch.object(requests, "put", return_value=fake_response)
@patch.object(AutoConfig, "__call__", return_value=None)
def test_update_ticket_with_comment(mocked_env, mocked_requests):
    fake_response.status_code = HTTPStatus.OK
    fake_response.json.return_value = stub_response
    response = JormungandrTransport.update_ticket_with_comment(dummy_jwt, dummy_ticket_id, dummy_comment)
    mocked_requests.assert_called_once_with(
        None,
        json={"body": dummy_comment, "id": dummy_ticket_id},
        headers={"x-thebes-answer": dummy_jwt}
    )
    assert response is True


@patch.object(requests, "put", return_value=fake_response)
@patch.object(AutoConfig, "__call__", return_value=None)
def test_update_ticket_with_comment_bad_status(mocked_env, mocked_requests):
    fake_response.status_code = HTTPStatus.BAD_REQUEST
    with pytest.raises(JormungandrCommunication):
        JormungandrTransport.update_ticket_with_comment(dummy_jwt, dummy_ticket_id, dummy_comment)
    mocked_requests.assert_called_once_with(
        None,
        json={"body": dummy_comment, "id": dummy_ticket_id},
        headers={"x-thebes-answer": dummy_jwt}
    )


@patch.object(requests, "put", side_effect=Exception())
@patch.object(AutoConfig, "__call__", return_value=None)
def test_update_ticket_impossible_to_reach_url(mocked_env, mocked_requests):
    with pytest.raises(JormungandrCommunication):
        JormungandrTransport.update_ticket_with_comment(dummy_jwt, dummy_ticket_id, dummy_comment)
    mocked_requests.assert_called_once_with(
        None,
        json={"body": dummy_comment, "id": dummy_ticket_id},
        headers={"x-thebes-answer": dummy_jwt}
    )