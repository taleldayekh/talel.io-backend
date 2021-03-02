from typing import Generator

import pytest

from talelio_backend.core.db import engine
from talelio_backend.data.orm import metadata


@pytest.fixture(scope='module', autouse=True)
def test_db() -> Generator:
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)
