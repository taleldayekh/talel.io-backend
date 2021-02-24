from typing import Generator

import pytest
from _pytest.fixtures import FixtureRequest

from talelio_backend.core import create_app
from talelio_backend.core.db import engine
from talelio_backend.data.orm import metadata


@pytest.fixture(scope='module', autouse=True)
def test_db() -> Generator:
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture(scope='class')
def api_server(request: FixtureRequest) -> None:
    app = create_app()
    app.config['TESTING'] = True
    request.cls.api = app.test_client()
