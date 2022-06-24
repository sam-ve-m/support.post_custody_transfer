from http import HTTPStatus

import pytest
import requests
from decouple import AutoConfig

from unittest.mock import patch, MagicMock
from func.src.domain.snapshot.model import Snapshots
from func.src.repository.snapshot.repository import SnapshotRepository


fake_response = MagicMock()
dummy_response = {"response": True}
stub_response = {"result": dummy_response}
dummy_jwt = "15919as5da95s1azsx591a9s51dfa"


@patch.object(requests, "get", return_value=fake_response)
@patch.object(Snapshots, "__init__", return_value=None)
@patch.object(AutoConfig, "__call__", return_value=None)
def test_request_snapshot(mocked_env, mocked_snapshot_validator, mocked_requests):
    fake_response.status_code = HTTPStatus.OK
    fake_response.json.return_value = stub_response
    SnapshotRepository.request_snapshot(dummy_jwt)
    mocked_requests.assert_called_once_with(None, headers={"x-thebes-answer": dummy_jwt})
    mocked_snapshot_validator.assert_called_once_with(**dummy_response)


@patch.object(requests, "get", return_value=fake_response)
@patch.object(Snapshots, "__init__", return_value=None)
@patch.object(AutoConfig, "__call__", return_value=None)
def test_request_snapshot_bad_status(mocked_env, mocked_snapshot_validator, mocked_requests):
    fake_response.status_code = HTTPStatus.BAD_REQUEST
    with pytest.raises(ValueError):
        SnapshotRepository.request_snapshot(dummy_jwt)
    mocked_requests.assert_called_once_with(None, headers={"x-thebes-answer": dummy_jwt})
    mocked_snapshot_validator.assert_not_called()
