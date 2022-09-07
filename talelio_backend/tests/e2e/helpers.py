# pylint: disable=E1101
from io import BytesIO
from typing import Dict, Optional, Union
from unittest.mock import patch

import pytest
from flask import Response

from talelio_backend.tests.constants import (ACCOUNTS_BASE_URL, ARTICLES_BASE_URL, ASSETS_BASE_URL,
                                             PROJECTS_BASE_URL, USERS_BASE_URL)


@pytest.mark.usefixtures('api_server')
class RequestHelper:

    def register_account_request(self,
                                 registration_data: Union[Dict[str, str],
                                                          None] = None) -> Response:
        with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
            request_payload = registration_data if registration_data else {}

            return self.api.post(  # type: ignore
                f'{ACCOUNTS_BASE_URL}/register', json=request_payload)

    def verify_account_request(self, verification_token: str) -> Response:
        return self.api.get(f'{ACCOUNTS_BASE_URL}/verify/{verification_token}')  # type: ignore

    def login_request(self, login_data: Union[Dict[str, str], None] = None) -> Response:
        request_payload = login_data if login_data else {}

        return self.api.post(f'{ACCOUNTS_BASE_URL}/login', json=request_payload)  # type: ignore

    def new_access_token_request(self, refresh_token_data: Union[str, None] = None) -> Response:
        self.api.cookie_jar.clear_session_cookies()  # type: ignore

        if refresh_token_data:
            self.api.set_cookie('', 'refresh_token', refresh_token_data)  # type: ignore

        return self.api.post(  # type: ignore
            f'{ACCOUNTS_BASE_URL}/token')

    def logout_request(self, authentication_header: Dict[str, str]) -> Response:
        return self.api.post(  # type: ignore
            f'{ACCOUNTS_BASE_URL}/logout', headers=authentication_header)

    def get_user_projects_request(self, username: str) -> Response:
        return self.api.get(f'{USERS_BASE_URL}/{username}/projects')  # type: ignore

    def get_user_articles_request(
            self,
            username: str,
            pagination_query_params: Optional[Union[str, None]] = None) -> Response:
        if pagination_query_params:
            url = f'{USERS_BASE_URL}/{username}/articles{pagination_query_params}'
        else:
            url = f'{USERS_BASE_URL}/{username}/articles'

        return self.api.get(url)  # type: ignore

    def create_project_request(self,
                               authorization_header: Dict[str, str],
                               project_data: Union[Dict[str, str], None] = None) -> Response:
        request_payload = project_data if project_data else {}

        return self.api.post(  # type: ignore
            PROJECTS_BASE_URL, headers=authorization_header, json=request_payload)

    def create_article_request(self,
                               authorization_header: Dict[str, str],
                               article_data: Union[Dict[str, str], None] = None) -> Response:
        request_payload = article_data if article_data else {}

        return self.api.post(  # type: ignore
            ARTICLES_BASE_URL, headers=authorization_header, json=request_payload)

    def get_article_request(self, slug: str) -> Response:
        return self.api.get(f'{ARTICLES_BASE_URL}/{slug}')  # type: ignore

    def upload_images_request(self, image_streams: Dict[str, BytesIO],
                              authorization_header: Dict[str, str]) -> Response:
        return self.api.post(  # type: ignore
            f'{ASSETS_BASE_URL}/images',
            headers=authorization_header,
            data=image_streams,
            content_type='multipart/form-data')
