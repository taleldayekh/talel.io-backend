from os import environ
from typing import Generator
from unittest.mock import patch

import pytest
from _pytest.fixtures import FixtureRequest
from boto3 import client
from flask.testing import FlaskClient
from moto import mock_aws

from talelio_backend import create_app
from talelio_backend.tests.constants import (EMAIL_BIANCA, EMAIL_TALEL, INVALID_EMAIL,
                                             S3_TEST_BUCKET)


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


@pytest.fixture
def mocked_s3(request: FixtureRequest) -> Generator:
    with mock_aws():
        s3 = client('s3')

        if request.param is None:  # type: ignore
            s3.create_bucket(Bucket=S3_TEST_BUCKET)
        else:
            location = {'LocationConstraint': request.param}  # type: ignore
            s3.create_bucket(Bucket=S3_TEST_BUCKET,
                             CreateBucketConfiguration=location)  # type: ignore

        yield s3
