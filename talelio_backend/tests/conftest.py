from os import environ
from typing import Generator
from unittest.mock import patch

import pytest
from _pytest.fixtures import FixtureRequest

from talelio_backend.core import create_app
from talelio_backend.tests.utils.constants import EMAIL


@pytest.fixture(scope='module', autouse=True)
def test_env_variables() -> Generator:
    mock_env_variables = {'WHITELISTED_EMAILS': EMAIL}

    with patch.dict(environ, mock_env_variables):
        yield


@pytest.fixture(scope='class')
def api_server(request: FixtureRequest) -> None:
    app = create_app()
    app.config['TESTING'] = True
    request.cls.api = app.test_client()
