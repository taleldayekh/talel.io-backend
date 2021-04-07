# pylint: disable=E1101
from typing import Dict
from unittest.mock import patch

import pytest
from flask import Response

from talelio_backend.tests.utils.constants import ACCOUNT_BASE_URL


@pytest.mark.usefixtures('api_server')
class RequestHelper:
    def register_account_request(self, registration_data: Dict[str, str]) -> Response:
        with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
            return self.api.post(  # type: ignore
                f'{ACCOUNT_BASE_URL}/register', json=registration_data)

    def verify_account_request(self, verification_token: str) -> Response:
        return self.api.get(f'{ACCOUNT_BASE_URL}/verify/{verification_token}')  # type: ignore

    def login_request(self, login_data: Dict[str, str]) -> Response:
        return self.api.post(f'{ACCOUNT_BASE_URL}/login', json=login_data)  # type: ignore
