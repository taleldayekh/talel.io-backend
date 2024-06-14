from re import findall
from unittest.mock import MagicMock, patch

import pytest
from boto3 import client
from flask import json

from talelio_backend.tests.constants import INVALID_USER, USERNAME_TALEL
from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.articles import fixed_or_rotary_wing_article, hiking_gear_article
from talelio_backend.tests.mocks.data import generate_file_streams

ASSET_STORE_DOWNLOAD = 'talelio_backend.app_assets.data.asset_store.AssetStore.download'


@pytest.mark.usefixtures('populate_db_account', 'populate_db_articles')
class TestGetUserArticles(RequestHelper):

    def test_can_get_user_articles(self) -> None:
        res = self.get_user_articles_request(USERNAME_TALEL)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert res_data['articles'][0]['title'] == hiking_gear_article['title']
        assert res_data['articles'][1]['title'] == fixed_or_rotary_wing_article['title']

    def test_can_get_paginated_user_articles(self) -> None:
        pagination_query_params = '?page=1&limit=3'
        res = self.get_user_articles_request(USERNAME_TALEL, pagination_query_params)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert len(res_data['articles']) == 3

    def test_header_includes_total_articles_count(self) -> None:
        res = self.get_user_articles_request(USERNAME_TALEL)
        res_data = json.loads(res.data)

        total_articles_count = res.headers['X-Total-Count']
        total_articles = len(res_data['articles'])

        assert int(total_articles_count) == total_articles

    def test_header_includes_next_and_prev_pagination(self) -> None:
        pagination_query_params = '?page=2&limit=2'
        res = self.get_user_articles_request(USERNAME_TALEL, pagination_query_params)

        # Retrieves pagination query params from URL
        header_pagination_query_params = findall(r'((?<=articles).*?(?=>))', res.headers['Link'])
        next_page_query_params = header_pagination_query_params[0]
        prev_page_query_params = header_pagination_query_params[1]

        assert 'page=3' in next_page_query_params
        assert 'page=1' in prev_page_query_params

    def test_out_of_range_pagination_returns_empty_response(self) -> None:
        pagination_query_params = '?page=666&limit=3'
        res = self.get_user_articles_request(USERNAME_TALEL, pagination_query_params)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert res_data == {}

    def test_non_existing_user_returns_empty_response(self) -> None:
        res = self.get_user_articles_request(INVALID_USER)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert res_data == {}

    def test_cannot_get_articles_with_invalid_pagination_query_params(self) -> None:
        invalid_pagination_query_params = '?page=one&limit=three'
        res = self.get_user_articles_request(USERNAME_TALEL, invalid_pagination_query_params)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Expected numeric query parameters'


@pytest.mark.usefixtures('populate_db_account')
class TestGetUserAssets(RequestHelper):
    images = [('image.jpeg', 0)]

    @patch(ASSET_STORE_DOWNLOAD)
    def test_can_get_user_image(self, mocked_asset_store_download: MagicMock) -> None:
        with generate_file_streams(self.images) as file_streams:
            image_file = file_streams[0]
            image_filename = image_file.name

            mocked_asset_store_download.return_value = image_file

            res = self.download_image_request(USERNAME_TALEL, image_filename)
            res_data = res.data

            assert res.status_code == 200
            assert isinstance(res_data, bytes)

    def test_cannot_get_image_for_non_existing_user(self) -> None:
        non_existing_user = 'non_existing_user'

        res = self.download_image_request(non_existing_user, 'image.jpeg')
        res_data = json.loads(res.data)

        assert res.status_code == 404
        assert res_data['error'][
            'message'] == f"User with username '{non_existing_user}' does not exist"

    @patch(ASSET_STORE_DOWNLOAD)
    def test_can_catch_s3_errors(self, mocked_asset_store_download: MagicMock) -> None:
        mocked_asset_store_download.side_effect = client('s3').exceptions.ClientError({'': ''}, '')

        res = self.download_image_request(USERNAME_TALEL, 'image.jpeg')
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert 'An error occurred' in res_data['error']['message']
