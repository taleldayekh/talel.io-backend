from typing import Generator
from unittest.mock import patch

import pytest
from flask.testing import FlaskClient

from talelio_backend.core.db import engine
from talelio_backend.data.orm import metadata
from talelio_backend.tests.utils.constants import ACCOUNTS_BASE_URL, USERNAME_TALEL, USERS_BASE_URL
from talelio_backend.tests.utils.mock_data import talel_registration_data, talelio_server_project


@pytest.fixture(scope='class', autouse=True)
def test_db() -> Generator:
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture(scope='class')
def populate_db_account(api_server: FlaskClient) -> None:
    with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
        api_server.post(f'{ACCOUNTS_BASE_URL}/register', json=talel_registration_data)


@pytest.fixture(scope='class')
def populate_db_project(api_server: FlaskClient) -> None:
    api_server.post(f'{USERS_BASE_URL}/{USERNAME_TALEL}/projects', json=talelio_server_project)
