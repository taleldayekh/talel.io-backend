from typing import Dict

import pytest
from flask import json

from talelio_backend.shared.utils import generate_slug
from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.articles import article_one, article_two
from talelio_backend.tests.utils import generate_authorization_header


@pytest.mark.usefixtures('populate_db_account')
class TestCreateArticle(RequestHelper):

    def test_can_create_article(self, authorization_header: Dict[str, str]) -> None:
        res = self.create_article_request(authorization_header, article_one)
        res_data = json.loads(res.data)

        assert res.status_code == 201
        assert res_data['title'] == article_one['title']
        assert res_data['body'] == article_one['body']

    def test_can_generate_slug_with_id_on_conflict(self, authorization_header: Dict[str,
                                                                                    str]) -> None:
        res_one = self.create_article_request(authorization_header, article_two)
        res_one_slug = json.loads(res_one.data)['slug']

        res_two = self.create_article_request(authorization_header, article_two)
        res_two_data = json.loads(res_two.data)
        res_two_id = res_two_data['id']

        assert res_two_data['slug'] == f'{res_one_slug}-{res_two_id}'

    def test_cannot_create_article_when_missing_details(
            self, authorization_header: Dict[str, str]) -> None:
        res = self.create_article_request(authorization_header, {'title': article_one['title']})
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
        res_no_authorization_header = self.create_article_request({}, article_one)
        res_no_authorization_header_data = json.loads(res_no_authorization_header.data)

        assert res_no_authorization_header.status_code == 403
        assert res_no_authorization_header_data['error'][
            'message'] == 'No authorization header provided'

        no_token_authorization_header = generate_authorization_header(no_token=True)
        res_no_token_authorization_header = self.create_article_request(
            no_token_authorization_header, article_one)
        res_no_token_authorization_header_data = json.loads(res_no_token_authorization_header.data)

        assert res_no_token_authorization_header.status_code == 403
        assert res_no_token_authorization_header_data['error'][
            'message'] == 'No authorization token provided'

        invalid_token_authorization_header = generate_authorization_header(invalid_token=True)
        res_invalid_token_authorization_header = self.create_article_request(
            invalid_token_authorization_header, article_one)

        assert res_invalid_token_authorization_header.status_code == 403


@pytest.mark.usefixtures('populate_db_account', 'populate_db_articles')
class TestGetArticle(RequestHelper):

    def test_can_get_article_by_slug(self) -> None:
        article_one_slug = generate_slug(article_one['title'])

        res = self.get_article_request(article_one_slug)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert res_data['title'] == article_one['title']
