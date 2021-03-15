# pylint: disable=E1101
from os import environ
from time import sleep
from unittest.mock import patch

import pytest
from flask import json

from talelio_backend.tests.utils.constants import (ACCOUNT_BASE_URL, EMAIL_BIANCA, EMAIL_TALEL,
                                                   PASSWORD)
from talelio_backend.tests.utils.mocks import generate_verification_token

account_registration_data = {'email': EMAIL_TALEL, 'password': PASSWORD}


@pytest.mark.usefixtures('api_server')
class TestAccountApiPOST:
    def test_valid_registration_email_api_request(self) -> None:
        with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
            res = self.api.post(  # type: ignore
                f'{ACCOUNT_BASE_URL}/register', json=account_registration_data)

            assert res.status_code == 200

    def test_cannot_send_registration_email_with_missing_registration_details(self) -> None:
        data = {'email': EMAIL_TALEL}

        with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
            res = self.api.post(f'{ACCOUNT_BASE_URL}/register', json=data)  # type: ignore
            res_data = json.loads(res.data)

            assert res.status_code == 400
            assert res_data['error']['message'] == "Expected 'password' key"


@pytest.mark.usefixtures('api_server')
class TestAccountApiGET:
    def test_valid_register_account_api_request(self) -> None:
        token = generate_verification_token(None, account_registration_data)
        res = self.api.get(f'{ACCOUNT_BASE_URL}/register/{token}')  # type: ignore

        assert res.status_code == 200

    def test_cannot_register_account_with_expired_registration_token(self) -> None:
        token = generate_verification_token(0, account_registration_data)

        # TODO: Replace sleep with mocked token expiration or a library like FreezeGun
        sleep(1)
        res = self.api.get(f'{ACCOUNT_BASE_URL}/register/{token}')  # type: ignore
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Invalid registration token'

    @patch.dict(environ, {'WHITELISTED_EMAILS': ''})
    def test_cannot_register_account_with_non_whitelisted_email(self) -> None:
        token = generate_verification_token(None, account_registration_data)
        res = self.api.get(f'{ACCOUNT_BASE_URL}/register/{token}')  # type: ignore
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Email not whitelisted'

    def test_cannot_register_account_with_previously_registered_email(self) -> None:
        token = generate_verification_token(None, {'email': EMAIL_BIANCA, 'password': PASSWORD})
        res_one = self.api.get(f'{ACCOUNT_BASE_URL}/register/{token}')  # type: ignore

        assert res_one.status_code == 200

        res_two = self.api.get(f'{ACCOUNT_BASE_URL}/register/{token}')  # type: ignore
        res_two_data = json.loads(res_two.data)

        assert res_two.status_code == 400
        assert res_two_data['error'][
            'message'] == f"Account with the email '{EMAIL_BIANCA}' already exists"
