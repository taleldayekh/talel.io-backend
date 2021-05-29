import pytest
from flask import json

from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.data import generate_file_streams
from talelio_backend.tests.utils import generate_authorization_header


@pytest.mark.usefixtures('populate_db_account')
class TestUploadImages(RequestHelper):
    images = [('image.jpeg', 0)]

    def test_cannot_upload_images_for_unauthorized_user(self) -> None:
        with generate_file_streams(self.images) as file_streams:
            res_no_authorization_header = self.upload_images_request(file_streams, {})
            res_no_authorization_header_data = json.loads(res_no_authorization_header.data)

            assert res_no_authorization_header.status_code == 403
            assert res_no_authorization_header_data['error'][
                'message'] == 'No authorization header provided'

        with generate_file_streams(self.images) as file_streams:
            no_token_authorization_header = generate_authorization_header(no_token=True)
            res_no_token_authorization_header = self.upload_images_request(
                file_streams, no_token_authorization_header)
            res_no_token_authorization_header_data = json.loads(
                res_no_token_authorization_header.data)

            assert res_no_token_authorization_header.status_code == 403
            assert res_no_token_authorization_header_data['error'][
                'message'] == 'No authorization token provided'

        with generate_file_streams(self.images) as file_streams:
            invalid_token_authorization_header = generate_authorization_header(invalid_token=True)
            res_invalid_token_authorization_header = self.upload_images_request(
                file_streams, invalid_token_authorization_header)

            assert res_invalid_token_authorization_header.status_code == 403


# TODO: Mock S3 and test API image upload success response and S3 ClientError
