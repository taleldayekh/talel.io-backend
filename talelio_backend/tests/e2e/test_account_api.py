# pylint: disable=E1101
from os import environ
from typing import Dict
from unittest.mock import patch

import pytest
from flask import Response, json

from talelio_backend.tests.utils.constants import (ACCOUNT_BASE_URL, EMAIL_BIANCA, EMAIL_TALEL,
                                                   PASSWORD, USERNAME_BIANCA, USERNAME_TALEL)
from talelio_backend.tests.utils.mocks import generate_verification_token

talel_account_registration_data = {
    'email': EMAIL_TALEL,
    'password': PASSWORD,
    'username': USERNAME_TALEL
}

bianca_account_registration_data = {
    'email': EMAIL_BIANCA,
    'password': PASSWORD,
    'username': USERNAME_BIANCA,
}

INVALID_EMAIL = 'unknown@unknown.unknown'


@pytest.mark.usefixtures('api_server')
class TestRequests:
    def make_register_request(self, account_registration_data: Dict[str, str]) -> Response:
        with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
            return self.api.post(  # type: ignore
                f'{ACCOUNT_BASE_URL}/register', json=account_registration_data)

    def make_verify_request(self, verification_token: str) -> Response:
        return self.api.get(f'{ACCOUNT_BASE_URL}/verify/{verification_token}')  # type: ignore


class TestAccountApiPOST(TestRequests):
    def test_valid_register_account_api_request(self) -> None:
        res = self.make_register_request(talel_account_registration_data)
        res_data = json.loads(res.data)

        assert res.status_code == 201
        assert res_data['email'] == EMAIL_TALEL
        assert res_data['user']['username'] == USERNAME_TALEL

    def test_cannot_register_account_with_missing_registration_details(self) -> None:
        res = self.make_register_request({'email': EMAIL_TALEL})
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == "Expected 'password' key"

    @patch.dict(environ, {'WHITELISTED_EMAILS': ''})
    def test_cannot_register_account_with_non_whitelisted_email(self) -> None:
        res = self.make_register_request(talel_account_registration_data)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Email not whitelisted'

    def test_cannot_register_account_with_already_registered_email(self) -> None:
        res_one = self.make_register_request(bianca_account_registration_data)

        assert res_one.status_code == 201

        res_two = self.make_register_request(bianca_account_registration_data)
        res_two_data = json.loads(res_two.data)

        assert res_two.status_code == 400
        assert res_two_data['error'][
            'message'] == f"Account with the email '{EMAIL_BIANCA}' already exists"


class TestAccountApiGET(TestRequests):
    def test_valid_verify_account_api_request(self) -> None:
        verification_token = generate_verification_token({'email': EMAIL_TALEL})

        not_verified_res = self.make_register_request(talel_account_registration_data)
        not_verified_res_data = json.loads(not_verified_res.data)

        assert not not_verified_res_data['verified']

        verified_res = self.make_verify_request(verification_token)
        verified_res_data = json.loads(verified_res.data)

        assert verified_res.status_code == 200
        assert verified_res_data['verified']

    def test_cannot_verify_non_registered_account(self) -> None:
        verification_token = generate_verification_token({'email': INVALID_EMAIL})

        res = self.make_verify_request(verification_token)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error'][
            'message'] == f"No registered account with the email '{INVALID_EMAIL}'"

    def test_cannot_verify_already_verified_account(self) -> None:
        verification_token = generate_verification_token({'email': EMAIL_BIANCA})

        self.make_register_request(bianca_account_registration_data)
        self.make_verify_request(verification_token)

        res = self.make_verify_request(verification_token)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Account already verified'
