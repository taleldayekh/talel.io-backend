from os import environ
from typing import Dict
from unittest.mock import patch

import pytest
from flask import json
from freezegun import freeze_time

from talelio_backend.identity_and_access.authentication import Authentication
from talelio_backend.shared.utils import generate_time_from_now
from talelio_backend.tests.constants import (EMAIL_BIANCA, EMAIL_TALEL, INITIAL_USER_ID,
                                             INVALID_EMAIL, PASSWORD, USERNAME_BIANCA,
                                             USERNAME_TALEL)
from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.accounts import (bianca_registration_data, talel_login_data,
                                                  talel_registration_data)
from talelio_backend.tests.mocks.projects import talelio_server_project
from talelio_backend.tests.utils import generate_authorization_header


@pytest.mark.usefixtures('populate_db_account')
class TestRegisterAccount(RequestHelper):
    def test_can_register_account(self) -> None:
        res = self.register_account_request(bianca_registration_data)
        res_data = json.loads(res.data)

        assert res.status_code == 201
        assert res_data['email'] == EMAIL_BIANCA
        assert res_data['user']['username'] == USERNAME_BIANCA

    def test_cannot_register_account_when_missing_registration_details(self) -> None:
        res = self.register_account_request({'email': EMAIL_TALEL})
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == "Expected 'password' key"

    def test_cannot_register_account_with_missing_request_body(self) -> None:
        res = self.register_account_request()
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == "Missing request body"

    @patch.dict(environ, {'WHITELISTED_EMAILS': ''})
    def test_cannot_register_account_with_non_whitelisted_email(self) -> None:
        res = self.register_account_request(bianca_registration_data)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Email not whitelisted'

    def test_cannot_register_account_with_already_registered_email(self) -> None:
        res = self.register_account_request(talel_registration_data)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error'][
            'message'] == f"Account with the email '{EMAIL_TALEL}' already exists"

    def test_cannot_register_account_with_already_registered_username(self) -> None:
        registration_data = {
            'email': INVALID_EMAIL,
            'password': PASSWORD,
            'username': USERNAME_TALEL
        }

        res = self.register_account_request(registration_data)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error'][
            'message'] == f"Account with the username '{USERNAME_TALEL}' already exists"


class TestVerifyAccount(RequestHelper):
    def test_can_verify_account(self) -> None:
        talel_verification_token = Authentication.generate_token({'email': EMAIL_TALEL})

        res_account = self.register_account_request(talel_registration_data)
        res_account_data = json.loads(res_account.data)

        assert not res_account_data['verified']

        res_verify = self.verify_account_request(talel_verification_token)
        res_verify_data = json.loads(res_verify.data)

        assert res_verify.status_code == 200
        assert res_verify_data['verified']

    def test_cannot_verify_non_registered_account(self) -> None:
        unknown_verification_token = Authentication.generate_token({'email': INVALID_EMAIL})

        res = self.verify_account_request(unknown_verification_token)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error'][
            'message'] == f"No registered account with the email '{INVALID_EMAIL}'"

    def test_cannot_verify_already_verified_account(self) -> None:
        bianca_verification_token = Authentication.generate_token({'email': EMAIL_BIANCA})

        self.register_account_request(bianca_registration_data)
        self.verify_account_request(bianca_verification_token)

        res = self.verify_account_request(bianca_verification_token)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Account already verified'

    def test_cannot_verify_account_with_invalid_token(self) -> None:
        invalid_verification_token = Authentication.generate_token({'email': EMAIL_TALEL},
                                                                   'invalidsecretkey')

        res = self.verify_account_request(invalid_verification_token)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Invalid verification token'


@pytest.mark.usefixtures('populate_db_account')
class TestLogin(RequestHelper):
    def test_can_login_to_account(self) -> None:
        res = self.login_request(talel_login_data)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert res_data['access_token']
        assert res.headers['Set-Cookie']

    def test_access_token_expires_30_min_after_login(self) -> None:
        res_login = self.login_request(talel_login_data)
        res_login_data = json.loads(res_login.data)
        access_token = res_login_data['access_token']

        thirtyone_mins_from_now = generate_time_from_now(1860)

        with freeze_time(thirtyone_mins_from_now):
            authorization_header = generate_authorization_header(access_token=access_token)
            res_proj = self.create_project_request(authorization_header, talelio_server_project)
            res_proj_data = json.loads(res_proj.data)

            assert res_proj.status_code == 403
            assert res_proj_data['error']['message'] == 'Signature has expired'

    def test_cannot_login_when_missing_login_details(self) -> None:
        invalid_login_data = {'email': talel_login_data['email']}

        res = self.login_request(invalid_login_data)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == "Expected 'password' key"

    def test_cannot_login_with_missing_request_body(self) -> None:
        res = self.login_request()
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Missing request body'

    def test_cannot_login_to_non_registered_account(self) -> None:
        invalid_login_data = {'email': INVALID_EMAIL, 'password': PASSWORD}

        res = self.login_request(invalid_login_data)
        res_data = json.loads(res.data)

        assert res.status_code == 401
        assert res_data['error']['message'] == 'Invalid username or password'

    def test_cannot_login_with_invalid_password(self) -> None:
        invalid_login_data = {
            'email': talel_login_data['email'],
            'password': talel_login_data['password'] + '1986'
        }

        res = self.login_request(invalid_login_data)
        res_data = json.loads(res.data)

        assert res.status_code == 401
        assert res_data['error']['message'] == 'Invalid username or password'


@pytest.mark.usefixtures('populate_db_account', 'login_user_talel')
class TestNewAccessToken(RequestHelper):
    def test_valid_refresh_token_can_generate_new_access_token(
            self, login_user_talel: Dict[str, str]) -> None:
        refresh_token = login_user_talel['refresh_token']

        res = self.new_access_token_request(refresh_token)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert res_data['access_token']

    def test_cannot_generate_new_access_token_with_invalid_refresh_token_for_user(self) -> None:
        invalid_refresh_token = Authentication.generate_token({
            'user_id': INITIAL_USER_ID,
            'username': USERNAME_TALEL
        })

        res = self.new_access_token_request(invalid_refresh_token)
        res_data = json.loads(res.data)

        assert res.status_code == 401
        assert res_data['error'][
            'message'] == 'Provided refresh token not matching stored refresh token'

    def test_cannot_generate_new_access_token_with_invalid_refresh_token_signature(
            self, login_user_talel: Dict[str, str]) -> None:
        refresh_token = login_user_talel['refresh_token'] + 'ABC'
        res = self.new_access_token_request(refresh_token)

        assert res.status_code == 400

    def test_cannot_generate_new_access_token_for_user_with_no_stored_refresh_token(self) -> None:
        invalid_refresh_token = Authentication.generate_token({
            'user_id': INITIAL_USER_ID + 1986,
            'username': USERNAME_TALEL
        })

        res = self.new_access_token_request(invalid_refresh_token)
        res_data = json.loads(res.data)

        assert res.status_code == 401
        assert res_data['error']['message'] == 'No stored refresh token for user'

    def test_cannot_generate_new_access_token_when_missing_refresh_token(self) -> None:
        res = self.new_access_token_request()

        assert res.status_code == 400


@pytest.mark.usefixtures('populate_db_account', 'login_user_talel')
class TestLogout(RequestHelper):
    def test_can_delete_refresh_token_on_logout(self, authorization_header: Dict[str,
                                                                                 str]) -> None:
        res = self.logout_request(authorization_header)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert res_data['message'] == 'Successfully logged out'

    def test_cannot_delete_refresh_token_on_logout_for_unauthorized_user(self) -> None:
        invalid_token_authorization_header = generate_authorization_header(invalid_token=True)
        res = self.logout_request(invalid_token_authorization_header)

        assert res.status_code == 403

    def test_cannot_delete_non_existing_refresh_token_on_logout(
            self, authorization_header: Dict[str, str]) -> None:
        self.logout_request(authorization_header)

        res = self.logout_request(authorization_header)
        res_data = json.loads(res.data)

        assert res.status_code == 409
        assert res_data['error']['message'] == 'No token to delete'
