from typing import Dict, Generator
from unittest.mock import patch

import pytest
from flask.testing import FlaskClient

from talelio_backend.core.db import engine
from talelio_backend.data.orm import metadata
from talelio_backend.tests.constants import ACCOUNTS_BASE_URL, PROJECTS_BASE_URL
from talelio_backend.tests.mocks.accounts import talel_registration_data
from talelio_backend.tests.mocks.projects import talelio_server_project
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
def populate_db_project(api_server: FlaskClient, authorization_header: Dict[str, str]) -> None:
    api_server.post(PROJECTS_BASE_URL, headers=authorization_header, json=talelio_server_project)
