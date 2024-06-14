from os import path
from typing import Dict
from unittest.mock import MagicMock, patch

import pytest
from boto3 import client
from flask import json

from talelio_backend.tests.constants import USERNAME_TALEL
from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.data import generate_file_streams
from talelio_backend.tests.utils import generate_authorization_header

ASSET_STORE_UPLOAD = 'talelio_backend.app_assets.data.asset_store.AssetStore.upload'
IMAGE_ASSET_API_BASE_URL = f'https://api.talel.io/v1/users/{USERNAME_TALEL}/images'


@pytest.mark.usefixtures('populate_db_account')
class TestUploadImages(RequestHelper):
    images = [('image.jpeg', 0)]

    @patch(ASSET_STORE_UPLOAD)
    def test_can_upload_single_image(self, mocked_asset_store_upload: MagicMock,
                                     authorization_header: Dict[str, str]) -> None:
        with generate_file_streams(self.images) as file_streams:
            image_file = {'image_file': file_streams[0]}

            res = self.upload_images_request(image_file, authorization_header)
            res_data = json.loads(res.data)

            filename_without_extension = path.splitext(file_streams[0].name)[0]

            assert res.status_code == 200
            assert f'{IMAGE_ASSET_API_BASE_URL}/{filename_without_extension}_' in res_data[
                'image_objects_urls'][0]

    @patch(ASSET_STORE_UPLOAD)
    def test_can_upload_multiple_images(self, mocked_asset_store_upload: MagicMock,
                                        authorization_header: Dict[str, str]) -> None:
        images = [('one.jpeg', 0), ('two.png', 0)]

        with generate_file_streams(images) as file_streams:
            image_files = {'image_file_one': file_streams[0], 'image_file_two': file_streams[1]}

            res = self.upload_images_request(image_files, authorization_header)
            res_data = json.loads(res.data)

            image_one_filename_without_extension = path.splitext(file_streams[0].name)[0]
            image_two_filename_without_extension = path.splitext(file_streams[1].name)[0]

            assert res.status_code == 200
            assert f'{IMAGE_ASSET_API_BASE_URL}/{image_one_filename_without_extension}_' in res_data[
                'image_objects_urls'][0]
            assert f'{IMAGE_ASSET_API_BASE_URL}/{image_two_filename_without_extension}_' in res_data[
                'image_objects_urls'][1]

    @patch(ASSET_STORE_UPLOAD)
    def test_can_catch_s3_errors(self, mocked_asset_store_upload: MagicMock,
                                 authorization_header: Dict[str, str]) -> None:
        mocked_asset_store_upload.side_effect = client('s3').exceptions.ClientError({'': ''}, '')

        with generate_file_streams(self.images) as file_streams:
            image_files = {'image_file': file_streams[0]}
            res = self.upload_images_request(image_files, authorization_header)
            res_data = json.loads(res.data)

            assert res.status_code == 400
            assert 'An error occurred' in res_data['error']['message']

    def test_cannot_upload_non_image_files(self, authorization_header: Dict[str, str]) -> None:
        with generate_file_streams([('document.pdf', 0)]) as file_streams:
            files = {'file': file_streams[0]}
            res = self.upload_images_request(files, authorization_header)
            res_data = json.loads(res.data)

            assert res.status_code == 400
            assert res_data['error']['message'] == 'One or more image files are of invalid type'

    def test_cannot_upload_images_for_unauthorized_user(self) -> None:
        with generate_file_streams(self.images) as file_streams:
            image_files = {'image_file': file_streams[0]}
            res_no_authorization_header = self.upload_images_request(image_files, {})
            res_no_authorization_header_data = json.loads(res_no_authorization_header.data)

            assert res_no_authorization_header.status_code == 403
            assert res_no_authorization_header_data['error'][
                'message'] == 'No authorization header provided'

        with generate_file_streams(self.images) as file_streams:
            image_files = {'image_file': file_streams[0]}
            no_token_authorization_header = generate_authorization_header(no_token=True)
            res_no_token_authorization_header = self.upload_images_request(
                image_files, no_token_authorization_header)
            res_no_token_authorization_header_data = json.loads(
                res_no_token_authorization_header.data)

            assert res_no_token_authorization_header.status_code == 403
            assert res_no_token_authorization_header_data['error'][
                'message'] == 'No authorization token provided'

        with generate_file_streams(self.images) as file_streams:
            image_files = {'image_file': file_streams[0]}
            invalid_token_authorization_header = generate_authorization_header(invalid_token=True)
            res_invalid_token_authorization_header = self.upload_images_request(
                image_files, invalid_token_authorization_header)

            assert res_invalid_token_authorization_header.status_code == 403
