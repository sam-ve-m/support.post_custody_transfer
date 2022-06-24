# Jormungandr
from ...domain.enums import CodeResponse

# Standards
import json

# Third party
from flask import Response
from nidavellir import Sindri


class ResponseModel:
    @staticmethod
    def build_response(success: bool, code: CodeResponse,  message: str) -> str:
        response_model = json.dumps(
            {
                "message": message,
                "success": success,
                "code": code.value,
            },
            default=Sindri.resolver,
        )
        return response_model

    @staticmethod
    def build_http_response(response_model: str, status: int, mimetype: str = "application/json") -> Response:
        response = Response(
            response_model,
            mimetype=mimetype,
            status=status.value,
        )
        return response
