import pytest
from _pytest.fixtures import FixtureRequest

from talelio_backend.core import create_app


@pytest.fixture(scope='class')
def api_server(request: FixtureRequest) -> None:
    app = create_app()
    app.config['TESTING'] = True
    request.cls.api = app.test_client()
