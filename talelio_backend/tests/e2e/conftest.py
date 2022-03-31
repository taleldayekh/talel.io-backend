from re import match
from typing import Dict, Generator
from unittest.mock import patch

import pytest
from flask.testing import FlaskClient

from talelio_backend.core.db import engine
from talelio_backend.shared.data.orm import metadata
from talelio_backend.tests.constants import ACCOUNTS_BASE_URL, ARTICLES_BASE_URL, PROJECTS_BASE_URL
from talelio_backend.tests.mocks.accounts import talel_login_data, talel_registration_data
from talelio_backend.tests.mocks.articles import (art_to_engineering_article,
                                                  private_blockchain_article)
from talelio_backend.tests.mocks.projects import talelio_client_project, talelio_server_project
from talelio_backend.tests.utils import generate_authorization_header


@pytest.fixture(scope='class', autouse=True)
def test_db() -> Generator:
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture(scope='class', name='authorization_header')
def fixture_authorization_header() -> Dict[str, str]:
    return generate_authorization_header()


@pytest.fixture(scope='class')
def populate_db_account(api_server: FlaskClient) -> None:
    with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
        api_server.post(f'{ACCOUNTS_BASE_URL}/register', json=talel_registration_data)


@pytest.fixture(scope='class')
def populate_db_projects(api_server: FlaskClient, authorization_header: Dict[str, str]) -> None:
    for project in [talelio_server_project, talelio_client_project]:
        api_server.post(PROJECTS_BASE_URL, headers=authorization_header, json=project)


@pytest.fixture(scope='class')
def populate_db_articles(api_server: FlaskClient, authorization_header: Dict[str, str]) -> None:
    for article in [art_to_engineering_article, private_blockchain_article]:
        api_server.post(ARTICLES_BASE_URL, headers=authorization_header, json=article)


@pytest.fixture(scope='class')
def login_user_talel(api_server: FlaskClient) -> Dict[str, str]:
    res = api_server.post(f'{ACCOUNTS_BASE_URL}/login', json=talel_login_data)

    cookie_header = res.headers['Set-Cookie'].split('=')[1]
    cookie_header_match = match('^.+?(?=;)', cookie_header)

    if cookie_header_match:
        refresh_token = cookie_header_match.group(0)

    return {'refresh_token': refresh_token}
