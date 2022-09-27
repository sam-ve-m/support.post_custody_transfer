from http import HTTPStatus

from unittest.mock import patch

import pytest
from werkzeug.local import LocalProxy

from decouple import RepositoryEnv, Config
import logging.config

with patch.object(Config, "__call__"):
    with patch.object(logging.config, "dictConfig"):
        with patch.object(RepositoryEnv, "__init__", return_value=None):
            from etria_logger import Gladsheim
            from main import post_user_ticket
            from src.domain.enums.enums import CodeResponse
            from src.domain.exceptions.exceptions import InvalidJwtToken, JormungandrCommunication, ErrorWithZendesk, \
    UnableToBuildSnapshot
            from src.domain.models.response.model import ResponseModel
            from src.domain.models.request.model import TicketValidator
            from src.services.jwt.service import JwtService
            from src.services.zendesk.service import CreateTicketService
            from src.services.snapshot.service import SnapshotUserDataService

dummy_jwt = "jwt"
dummy_decoded_jwt = "jwt"
open_ticket_response = True
dummy_response_model = "response_model"
dummy_model = "model"
dummy_snapshot = "snapshot"


@patch.object(JwtService, "apply_authentication_rules")
@patch.object(JwtService, "decode_jwt", return_value=dummy_decoded_jwt)
@patch.object(CreateTicketService, "set_tickets", return_value=open_ticket_response)
@patch.object(SnapshotUserDataService, "get_snapshot", return_value=dummy_snapshot)
@patch.object(ResponseModel, "build_response", return_value=dummy_response_model)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_model)
@patch.object(LocalProxy, "__init__")
@patch.object(TicketValidator, "__init__", return_value=None)
def test_post_user_ticket(
        mocked_requests,
        mocked_validator,
        mocked_build_http_response,
        mocked_build_response,
        mocked_snapshot_user_data,
        mocked_open_ticket_service,
        mocked_decode_jwt,
        mocked_apply_authentication_rules,
        monkeypatch
):
    setattr(LocalProxy, "json", {})
    setattr(LocalProxy, "headers", {"x-thebes-answer": dummy_jwt})
    response = post_user_ticket()
    mocked_apply_authentication_rules.assert_called_with(jwt=dummy_jwt)
    mocked_decode_jwt.assert_called_with(jwt=dummy_jwt)
    mocked_open_ticket_service.assert_called()
    mocked_snapshot_user_data.assert_called()
    mocked_build_response.assert_called_with(
        success=open_ticket_response, code=CodeResponse.SUCCESS, message="Ticket posted successfully"
    )
    mocked_build_http_response.assert_called_with(response_model=dummy_response_model, status=HTTPStatus.CREATED)
    assert response == dummy_model


dummy_invalid_jwt_exception = InvalidJwtToken()
dummy_invalid_jwt_exception_message = 'Failed to validate user credentials'
dummy_invalid_jwt_message = "Jormungandr::post_user_ticket::Invalid JWT token"


@patch.object(JwtService, "apply_authentication_rules", side_effect=dummy_invalid_jwt_exception)
@patch.object(ResponseModel, "build_response", return_value=dummy_response_model)
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "build_http_response", return_value=dummy_model)
@patch.object(LocalProxy, "__init__")
@patch.object(TicketValidator, "__init__", return_value=None)
def test_post_user_ticket_invalid_jwt(
        mocked_requests,
        mocked_validator,
        mocked_build_http_response,
        mocked_logger,
        mocked_build_response,
        mocked_apply_authentication_rules,
        monkeypatch
):
    setattr(LocalProxy, "json", {})
    setattr(LocalProxy, "headers", {"x-thebes-answer": dummy_jwt})
    response = post_user_ticket()
    mocked_apply_authentication_rules.assert_called_with(jwt=dummy_jwt)
    mocked_logger.assert_called_with(error=dummy_invalid_jwt_exception, message=dummy_invalid_jwt_message)
    mocked_build_response.assert_called_with(
        success=False, code=CodeResponse.JWT_INVALID, message=dummy_invalid_jwt_exception_message
    )
    mocked_build_http_response.assert_called_with(response_model=dummy_response_model, status=HTTPStatus.UNAUTHORIZED)
    assert response == dummy_model


dummy_common_exception = Exception()
dummy_common_exception_message = "Unexpected error occurred"
dummy_common_message = "Jormungandr::post_user_ticket::"

dummy_jormungandr_exception = JormungandrCommunication()
dummy_jormungandr_exception_message = "Unable to communicate with other Jormungandr fission"
dummy_zendesk_exception = ErrorWithZendesk()
dummy_zendesk_exception_message = "Unable to execute an action in Zendesk"
dummy_builder_exception = UnableToBuildSnapshot()
dummy_builder_exception_message = "Error while building snapshot"


@patch.object(JwtService, "apply_authentication_rules")
@patch.object(JwtService, "decode_jwt", return_value=dummy_decoded_jwt)
@patch.object(CreateTicketService, "set_tickets", side_effect=dummy_common_exception)
@patch.object(SnapshotUserDataService, "get_snapshot", return_value=dummy_snapshot)
@patch.object(ResponseModel, "build_response", return_value=dummy_response_model)
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "build_http_response", return_value=dummy_model)
@patch.object(LocalProxy, "__init__")
@patch.object(TicketValidator, "__init__", return_value=None)
def test_post_user_ticket_execution_error(
        mocked_requests,
        mocked_validator,
        mocked_build_http_response,
        mocked_logger,
        mocked_build_response,
        mocked_snapshot_user_data,
        mocked_open_ticket_service,
        mocked_decode_jwt,
        mocked_apply_authentication_rules,
        monkeypatch
):
    setattr(LocalProxy, "json", {})
    setattr(LocalProxy, "headers", {"x-thebes-answer": dummy_jwt})
    response = post_user_ticket()
    mocked_apply_authentication_rules.assert_called_with(jwt=dummy_jwt)
    mocked_decode_jwt.assert_called_with(jwt=dummy_jwt)
    mocked_open_ticket_service.assert_called()
    mocked_snapshot_user_data.assert_called()
    mocked_logger.assert_called_with(error=dummy_common_exception, message=dummy_common_message)
    mocked_build_response.assert_called_with(
        success=False, code=CodeResponse.INTERNAL_SERVER_ERROR, message=dummy_common_exception_message
    )
    mocked_build_http_response.assert_called_with(response_model=dummy_response_model,
                                                  status=HTTPStatus.INTERNAL_SERVER_ERROR)
    assert response == dummy_model


@pytest.mark.parametrize("exception,exception_message", [
    (dummy_builder_exception, dummy_builder_exception_message),
    (dummy_jormungandr_exception, dummy_jormungandr_exception_message),
])
@patch.object(JwtService, "apply_authentication_rules")
@patch.object(JwtService, "decode_jwt", return_value=dummy_decoded_jwt)
@patch.object(CreateTicketService, "set_tickets")
@patch.object(SnapshotUserDataService, "get_snapshot", return_value=dummy_snapshot)
@patch.object(ResponseModel, "build_response", return_value=dummy_response_model)
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "build_http_response", return_value=dummy_model)
@patch.object(LocalProxy, "__init__")
@patch.object(TicketValidator, "__init__", return_value=None)
def test_post_user_ticket_jormungandr_error(
        mocked_requests,
        mocked_validator,
        mocked_build_http_response,
        mocked_logger,
        mocked_build_response,
        mocked_snapshot_user_data,
        mocked_open_ticket_service,
        mocked_decode_jwt,
        mocked_apply_authentication_rules,
        exception,
        exception_message,
        monkeypatch
):
    mocked_open_ticket_service.side_effect = exception
    setattr(LocalProxy, "json", {})
    setattr(LocalProxy, "headers", {"x-thebes-answer": dummy_jwt})
    response = post_user_ticket()
    mocked_apply_authentication_rules.assert_called_with(jwt=dummy_jwt)
    mocked_decode_jwt.assert_called_with(jwt=dummy_jwt)
    mocked_open_ticket_service.assert_called()
    mocked_snapshot_user_data.assert_called()
    mocked_logger.assert_called_with(ex=exception, message=dummy_common_message+exception_message)
    mocked_build_response.assert_called_with(
        success=False, code=CodeResponse.PARTNERS_ERROR_ON_API_REQUEST, message=exception_message
    )
    mocked_build_http_response.assert_called_with(response_model=dummy_response_model,
                                                  status=HTTPStatus.SERVICE_UNAVAILABLE)
    assert response == dummy_model


@patch.object(JwtService, "apply_authentication_rules")
@patch.object(JwtService, "decode_jwt", return_value=dummy_decoded_jwt)
@patch.object(CreateTicketService, "set_tickets", side_effect=dummy_zendesk_exception)
@patch.object(SnapshotUserDataService, "get_snapshot", return_value=dummy_snapshot)
@patch.object(ResponseModel, "build_response", return_value=dummy_response_model)
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "build_http_response", return_value=dummy_model)
@patch.object(LocalProxy, "__init__")
@patch.object(TicketValidator, "__init__", return_value=None)
def test_post_user_ticket_zendesk_error(
        mocked_requests,
        mocked_validator,
        mocked_build_http_response,
        mocked_logger,
        mocked_build_response,
        mocked_snapshot_user_data,
        mocked_open_ticket_service,
        mocked_decode_jwt,
        mocked_apply_authentication_rules,
        monkeypatch
):
    setattr(LocalProxy, "json", {})
    setattr(LocalProxy, "headers", {"x-thebes-answer": dummy_jwt})
    response = post_user_ticket()
    mocked_apply_authentication_rules.assert_called_with(jwt=dummy_jwt)
    mocked_decode_jwt.assert_called_with(jwt=dummy_jwt)
    mocked_open_ticket_service.assert_called()
    mocked_snapshot_user_data.assert_called()
    mocked_logger.assert_called_with(ex=dummy_zendesk_exception, message=dummy_common_message+dummy_zendesk_exception_message)
    mocked_build_response.assert_called_with(
        success=False, code=CodeResponse.PARTNERS_ERROR_ON_API_REQUEST, message=dummy_zendesk_exception_message
    )
    mocked_build_http_response.assert_called_with(response_model=dummy_response_model,
                                                  status=HTTPStatus.SERVICE_UNAVAILABLE)
    assert response == dummy_model


dummy_params_exception = ValueError()
dummy_params_exception_message = "There are invalid format or extra/missing parameters"
dummy_params_message = "Jormungandr::post_user_ticket::There are invalid format or extra parameters"


@patch.object(JwtService, "apply_authentication_rules")
@patch.object(JwtService, "decode_jwt", return_value=dummy_decoded_jwt)
@patch.object(CreateTicketService, "set_tickets", side_effect=dummy_common_exception)
@patch.object(ResponseModel, "build_response", return_value=dummy_response_model)
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "build_http_response", return_value=dummy_model)
@patch.object(LocalProxy, "__init__")
@patch.object(TicketValidator, "__init__", side_effect=dummy_params_exception)
def test_post_user_ticket_invalid_params(
        mocked_validator,
        mocked_requests,
        mocked_build_http_response,
        mocked_logger,
        mocked_build_response,
        mocked_open_ticket_service,
        mocked_decode_jwt,
        mocked_apply_authentication_rules,
        monkeypatch
):
    setattr(LocalProxy, "json", {})
    setattr(LocalProxy, "headers", {"x-thebes-answer": dummy_jwt})
    response = post_user_ticket()
    mocked_apply_authentication_rules.assert_not_called()
    mocked_decode_jwt.assert_not_called()
    mocked_open_ticket_service.assert_not_called()
    mocked_logger.assert_called_with(ex=dummy_params_exception, message=dummy_params_message)
    mocked_build_response.assert_called_with(
        success=False, code=CodeResponse.INVALID_PARAMS, message=dummy_params_exception_message
    )
    mocked_build_http_response.assert_called_with(response_model=dummy_response_model,
                                                  status=HTTPStatus.BAD_REQUEST)
    assert response == dummy_model
