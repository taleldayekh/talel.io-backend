from typing import Dict

import pytest
from flask import json

from talelio_backend.shared.utils import generate_slug
from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.articles import (art_to_engineering_article,
                                                  private_blockchain_article)
from talelio_backend.tests.mocks.example_markdown import PRIVATE_BLOCKCHAIN_FEATURED_IMAGE_URL
from talelio_backend.tests.utils import generate_authorization_header


@pytest.mark.usefixtures('populate_db_account')
class TestCreateArticle(RequestHelper):

    def test_can_create_article(self, authorization_header: Dict[str, str]) -> None:
        res = self.create_article_request(authorization_header, art_to_engineering_article)
        res_data = json.loads(res.data)

        assert res.status_code == 201
        assert res_data['title'] == art_to_engineering_article['title']
        assert res_data['body'] == art_to_engineering_article['body']
        assert res_data['meta_description'] == art_to_engineering_article['meta_description']

    def test_can_generate_slug_with_id_on_conflict(self, authorization_header: Dict[str,
                                                                                    str]) -> None:
        res_one = self.create_article_request(authorization_header, private_blockchain_article)
        res_one_slug = json.loads(res_one.data)['slug']

        res_two = self.create_article_request(authorization_header, private_blockchain_article)
        res_two_data = json.loads(res_two.data)
        res_two_id = res_two_data['id']

        assert res_two_data['slug'] == f'{res_one_slug}-{res_two_id}'

    def test_can_provide_featured_image(self, authorization_header: Dict[str, str]) -> None:
        provided_featured_image = 'https://url/to/provided-featured-image.jpg'

        art_to_engineering_article_copy = dict(art_to_engineering_article)
        art_to_engineering_article_copy['featured_image'] = provided_featured_image

        res = self.create_article_request(authorization_header, art_to_engineering_article_copy)
        res_data = json.loads(res.data)

        assert res_data['featured_image'] == provided_featured_image

    def test_can_generate_featured_image_from_article_body(
            self, authorization_header: Dict[str, str]) -> None:
        res = self.create_article_request(authorization_header, private_blockchain_article)
        res_data = json.loads(res.data)

        assert res_data['featured_image'] == PRIVATE_BLOCKCHAIN_FEATURED_IMAGE_URL

    def test_can_create_article_with_no_featured_image(
            self, authorization_header: Dict[str, str]) -> None:
        res = self.create_article_request(authorization_header, art_to_engineering_article)
        res_data = json.loads(res.data)

        assert not res_data['featured_image']

    def test_cannot_create_article_when_missing_details(
            self, authorization_header: Dict[str, str]) -> None:
        res = self.create_article_request(authorization_header,
                                          {'title': art_to_engineering_article['title']})
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == "Expected 'body' key"

    def test_cannot_create_article_with_missing_request_body(
            self, authorization_header: Dict[str, str]) -> None:
        res = self.create_article_request(authorization_header)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Missing request body'

    def test_cannot_create_article_for_unauthorized_user(self) -> None:
        res_no_authorization_header = self.create_article_request({}, art_to_engineering_article)
        res_no_authorization_header_data = json.loads(res_no_authorization_header.data)

        assert res_no_authorization_header.status_code == 403
        assert res_no_authorization_header_data['error'][
            'message'] == 'No authorization header provided'

        no_token_authorization_header = generate_authorization_header(no_token=True)
        res_no_token_authorization_header = self.create_article_request(
            no_token_authorization_header, art_to_engineering_article)
        res_no_token_authorization_header_data = json.loads(res_no_token_authorization_header.data)

        assert res_no_token_authorization_header.status_code == 403
        assert res_no_token_authorization_header_data['error'][
            'message'] == 'No authorization token provided'

        invalid_token_authorization_header = generate_authorization_header(invalid_token=True)
        res_invalid_token_authorization_header = self.create_article_request(
            invalid_token_authorization_header, art_to_engineering_article)

        assert res_invalid_token_authorization_header.status_code == 403


@pytest.mark.usefixtures('populate_db_account', 'populate_db_articles')
class TestGetArticle(RequestHelper):

    def test_can_get_article_by_slug(self) -> None:
        article_slug = generate_slug(art_to_engineering_article['title'])

        res = self.get_article_request(article_slug)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert res_data['title'] == art_to_engineering_article['title']
