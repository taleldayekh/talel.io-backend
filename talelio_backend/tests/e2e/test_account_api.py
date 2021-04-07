from os import environ
from unittest.mock import patch

from flask import Response, json

from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.utils.constants import (EMAIL_BIANCA, EMAIL_TALEL, INVALID_EMAIL,
                                                   PASSWORD, USERNAME_BIANCA, USERNAME_TALEL)
from talelio_backend.tests.utils.mocks import generate_verification_token

talel_registration_data = {'email': EMAIL_TALEL, 'password': PASSWORD, 'username': USERNAME_TALEL}

bianca_registration_data = {
    'email': EMAIL_BIANCA,
    'password': PASSWORD,
    'username': USERNAME_BIANCA,
}

talel_login_data = {
    'email': talel_registration_data['email'],
    'password': talel_registration_data['password']
}


class TestRegisterAccount(RequestHelper):
    register_account_res: Response

    def setup_method(self) -> None:
        self.register_account_res = self.register_account_request(talel_registration_data)

    def test_can_register_account(self) -> None:
        res_data = json.loads(self.register_account_res.data)

        assert self.register_account_res.status_code == 201
        assert res_data['email'] == EMAIL_TALEL
        assert res_data['user']['username'] == USERNAME_TALEL

    def test_cannot_register_account_when_missing_registration_details(self) -> None:
        res = self.register_account_request({'email': EMAIL_TALEL})
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == "Expected 'password' key"

    @patch.dict(environ, {'WHITELISTED_EMAILS': ''})
    def test_cannot_register_account_with_non_whitelisted_email(self) -> None:
        res = self.register_account_request(bianca_registration_data)
        res_data = json.loads(res.data)

        assert self.register_account_res.status_code == 400
        assert res_data['error']['message'] == 'Email not whitelisted'

    def test_cannot_register_account_with_already_registered_email(self) -> None:
        res = self.register_account_request(talel_registration_data)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error'][
            'message'] == f"Account with the email '{EMAIL_TALEL}' already exists"


class TestVerifyAccount(RequestHelper):
    register_account_res: Response
    talel_verification_token: str
    unknown_verification_token: str
    invalid_verification_token: str

    def setup_method(self) -> None:
        self.register_account_res = self.register_account_request(talel_registration_data)
        self.talel_verification_token = generate_verification_token({'email': EMAIL_TALEL})
        self.unknown_verification_token = generate_verification_token({'email': INVALID_EMAIL})
        self.invalid_verification_token = generate_verification_token({'email': EMAIL_TALEL},
                                                                      'invalidsecretkey')

    def test_can_verify_account(self) -> None:
        register_account_res_data = json.loads(self.register_account_res.data)

        assert not register_account_res_data['verified']

        verify_account_res = self.verify_account_request(self.talel_verification_token)
        verify_account_res_data = json.loads(verify_account_res.data)

        assert verify_account_res.status_code == 200
        assert verify_account_res_data['verified']

    def test_cannot_verify_non_registered_account(self) -> None:
        res = self.verify_account_request(self.unknown_verification_token)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error'][
            'message'] == f"No registered account with the email '{INVALID_EMAIL}'"

    def test_cannot_verify_already_verified_account(self) -> None:
        res = self.verify_account_request(self.talel_verification_token)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Account already verified'

    def test_cannot_verify_account_with_invalid_token(self) -> None:
        res = self.verify_account_request(self.invalid_verification_token)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Invalid verification token'


class TestLogin(RequestHelper):
    def setup_method(self) -> None:
        self.register_account_request(talel_registration_data)

    def test_can_login_to_account(self) -> None:
        res = self.login_request(talel_login_data)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert res_data['access_token']

    def test_cannot_login_when_missing_login_details(self) -> None:
        invalid_login_data = {'email': talel_login_data['email']}

        res = self.login_request(invalid_login_data)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == "Expected 'password' key"

    def test_cannot_login_to_non_registered_account(self) -> None:
        invalid_login_data = {'email': INVALID_EMAIL, 'password': PASSWORD}

        res = self.login_request(invalid_login_data)
        res_data = json.loads(res.data)

        assert res.status_code == 401
        assert res_data['error']['message'] == 'Invalid username or password'

    def test_cannot_login_with_invalid_password(self) -> None:
        invalid_login_data = {
            'email': talel_registration_data['email'],
            'password': talel_registration_data['password'] + '1986'
        }

        res = self.login_request(invalid_login_data)
        res_data = json.loads(res.data)

        assert res.status_code == 401
        assert res_data['error']['message'] == 'Invalid username or password'
