# Standards
import json
from unittest.mock import MagicMock, patch

# Third party
from flask import Response
from nidavellir import Sindri

# Jormungandr
from func.src.domain.response.model import ResponseModel


dummy_response_code = 200
stub_response_code = MagicMock(value=dummy_response_code)
dummy_message = "done"
dummy_success = True
dummy_result = {}

fake_dumps = MagicMock(return_value=True)


@patch.object(json, "dumps", return_value=True)
@patch.object(Sindri, "resolver")
def test_build_response(mocked_resolver, mocked_dumps):
    response = ResponseModel.build_response(dummy_success, stub_response_code, dummy_message)
    mocked_dumps.assert_called_once_with(
        {"message": dummy_message, "success": dummy_success, "code": dummy_response_code},
        default=mocked_resolver
    )
    assert response is True


dummy_response_model = "response_model"
dummy_mimetype = "mimetype"


@patch.object(Response, "__init__", return_value=None)
def test_build_http_response(mocked_response_model):
    ResponseModel.build_http_response(dummy_response_model, stub_response_code, dummy_mimetype)
    mocked_response_model.assert_called_once_with(
        dummy_response_model,
        mimetype=dummy_mimetype,
        status=dummy_response_code,
    )
