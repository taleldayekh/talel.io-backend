from typing import Dict, NewType, Tuple

from flask import Flask, jsonify

ErrorResponseType = NewType('ErrorResponseType', Dict[str, Dict[str, object]])


class APIError(Exception):
    http_response_status_codes = {400: 'Bad Request'}

    def __init__(self, message: str, status_code: int) -> None:
        super().__init__()
        self.status_code = status_code
        self.status_type = self.http_response_status_codes[status_code]
        self.message = message

    @property
    def error_response(self) -> ErrorResponseType:
        return ErrorResponseType(
            dict(error=dict(status=self.status_code, type=self.status_type, message=self.message)))


def error_handlers(app: Flask) -> None:
    def api_error(error: APIError) -> Tuple[ErrorResponseType, int]:
        error_response = jsonify(error.error_response)
        return error_response, error.status_code

    app.errorhandler(APIError)(api_error)