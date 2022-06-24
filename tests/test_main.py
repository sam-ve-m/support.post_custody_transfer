# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from unittest.mock import patch
from werkzeug.local import LocalProxy

# Jormungandr
from func.main import post_user_ticket
from func.src.domain.validator import TicketValidator
from func.src.services.jwt import JwtService
from func.src.domain.enums import CodeResponse
from func.src.domain.exceptions import InvalidJwtToken
from func.src.domain.response.model import ResponseModel
from func.src.services.post_user_ticket import CreateTicketService
from func.src.services.snapshot import SnapshotUserDataService

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
