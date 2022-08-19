# Jormungandr
from unittest.mock import patch, MagicMock

# Third party
import pytest
from decouple import RepositoryEnv, Config
import logging.config

with patch.object(Config, "__call__"):
    with patch.object(logging.config, "dictConfig"):
        with patch.object(RepositoryEnv, "__init__", return_value=None):
            from heimdall_client import Heimdall
            from src.services.jwt.service import JwtService
            from src.domain.exceptions.exceptions import InvalidJwtToken

dummy_jwt = "jwt"
dummy_decoded_jwt = {"value": 1}
stub_jwt_content = {"decoded_jwt": dummy_decoded_jwt}
stub_jwt_missing_content = {"decoded_jwt": False}
fake_event_loop = MagicMock()


@patch.object(Heimdall, "decode_payload")
def test_decode_jwt(mocked_heimdall, monkeypatch):
    fake_event_loop.run_until_complete.return_value = stub_jwt_content, 200
    monkeypatch.setattr(JwtService, "event_loop", fake_event_loop)
    response = JwtService.decode_jwt(dummy_jwt)
    mocked_heimdall.assert_called_once_with(jwt=dummy_jwt)
    assert response == dummy_decoded_jwt


@patch.object(Heimdall, "decode_payload")
def test_decode_jwt_with_invalid_jwt(mocked_heimdall, monkeypatch):
    fake_event_loop.run_until_complete.return_value = stub_jwt_missing_content, 404
    monkeypatch.setattr(JwtService, "event_loop", fake_event_loop)
    with pytest.raises(InvalidJwtToken):
        JwtService.decode_jwt(dummy_jwt)
    mocked_heimdall.assert_called_once_with(jwt=dummy_jwt)


@patch.object(Heimdall, "validate_jwt")
def test_apply_authentication_rules(mocked_heimdall, monkeypatch):
    fake_event_loop.run_until_complete.return_value = True
    monkeypatch.setattr(JwtService, "event_loop", fake_event_loop)
    response = JwtService.apply_authentication_rules(dummy_jwt)
    mocked_heimdall.assert_called_once_with(jwt=dummy_jwt)
    assert response is None


@patch.object(Heimdall, "validate_jwt")
def test_apply_authentication_rules_invalid(mocked_heimdall, monkeypatch):
    fake_event_loop.run_until_complete.return_value = False
    monkeypatch.setattr(JwtService, "event_loop", fake_event_loop)
    with pytest.raises(InvalidJwtToken):
        JwtService.apply_authentication_rules(dummy_jwt)
    mocked_heimdall.assert_called_once_with(jwt=dummy_jwt)
