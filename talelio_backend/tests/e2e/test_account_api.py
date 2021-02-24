# pylint: disable=E1101
from os import getenv
from time import sleep
from typing import cast
from unittest.mock import patch

import pytest
from flask import json
from itsdangerous import TimedJSONWebSignatureSerializer

from talelio_backend.tests.utils.constants import ACCOUNT_BASE_URL, EMAIL, PASSWORD

SECRET_KEY = cast(str, getenv('SECRET_KEY'))
account_registration_data = {'email': EMAIL, 'password': PASSWORD}


@pytest.mark.usefixtures('api_server')
class TestAccountApiPOST:
    def test_valid_registration_email_api_request(self) -> None:
        with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
            res = self.api.post(  # type: ignore
                f'{ACCOUNT_BASE_URL}/register', json=account_registration_data)

            assert res.status_code == 200

    def test_cannot_send_registration_email_with_missing_registration_details(self) -> None:
        data = {'email': EMAIL}

        with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
            res = self.api.post(f'{ACCOUNT_BASE_URL}/register', json=data)  # type: ignore
            res_data = json.loads(res.data)

            assert res.status_code == 400
            assert res_data['error']['message'] == "Expected 'password' key"


@pytest.mark.usefixtures('api_server')
class TestAccountApiGET:
    def test_valid_register_account_api_request(self) -> None:
        serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, None)
        token = str(serializer.dumps(account_registration_data), 'utf-8')

        res = self.api.get(f'{ACCOUNT_BASE_URL}/register/{token}')  # type: ignore

        assert res.status_code == 200

    def test_cannot_register_account_with_expired_token(self) -> None:
        serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, 0)
        token = str(serializer.dumps(account_registration_data), 'utf-8')

        # TODO: Replace sleep with mocked token expiration or a library like FreezeGun
        sleep(1)
        res = self.api.get(f'{ACCOUNT_BASE_URL}/register/{token}')  # type: ignore
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Invalid registration token'
