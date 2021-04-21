from os import environ
from typing import Generator
from unittest.mock import patch

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient

from talelio_backend.core import create_app
from talelio_backend.tests.utils.constants import EMAIL_BIANCA, EMAIL_TALEL, INVALID_EMAIL


@pytest.fixture(scope='module', autouse=True)
def test_env_variables() -> Generator:
    mock_env_variables = {'WHITELISTED_EMAILS': f'{EMAIL_TALEL},{EMAIL_BIANCA},{INVALID_EMAIL}'}

    with patch.dict(environ, mock_env_variables):
        yield


@pytest.fixture(scope='class')
def api_server(request: FixtureRequest) -> FlaskClient:
    app = create_app()
    app.config['TESTING'] = True
    request.cls.api = app.test_client()
    return request.cls.api
