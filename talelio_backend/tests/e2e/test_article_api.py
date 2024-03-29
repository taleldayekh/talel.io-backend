from typing import Dict

import pytest
from flask import json

from talelio_backend.shared.utils.slug import generate_slug
from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.articles import (art_to_engineering_article, articles,
                                                  hiking_gear_article, private_blockchain_article)
from talelio_backend.tests.utils import generate_authorization_header


@pytest.mark.usefixtures('populate_db_account')
class TestCreateArticle(RequestHelper):

    def test_can_create_article(self, authorization_header: Dict[str, str]) -> None:
        res = self.create_article_request(authorization_header, art_to_engineering_article)
        res_data = json.loads(res.data)

        assert res.status_code == 201
        assert res_data['article']['title'] == art_to_engineering_article['title']
        assert res_data['article']['body'] == art_to_engineering_article['body']
        assert res_data['article']['meta_description'] == art_to_engineering_article[
            'meta_description']
        assert res_data['article']['featured_image'] == art_to_engineering_article[
            'featured_image']

    def test_can_generate_slug_with_incremental_number_suffix_on_conflict(
            self, authorization_header: Dict[str, str]) -> None:
        res_one = self.create_article_request(authorization_header, private_blockchain_article)
        res_one_slug = json.loads(res_one.data)['article']['slug']

        res_two = self.create_article_request(authorization_header, private_blockchain_article)
        res_two_data = json.loads(res_two.data)

        res_three = self.create_article_request(authorization_header, private_blockchain_article)
        res_three_data = json.loads(res_three.data)

        assert res_two_data['article']['slug'] == f'{res_one_slug}-2'
        assert res_three_data['article']['slug'] == f'{res_one_slug}-3'

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
        article_slug = generate_slug(hiking_gear_article['title'])

        res = self.get_article_request(article_slug)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert res_data['article']['title'] == hiking_gear_article['title']

    def test_article_meta_includes_prev_and_next_article(self) -> None:
        article_slug = generate_slug(articles[1]['title'])

        prev_article_title = articles[0]['title']
        next_article_title = articles[2]['title']

        res = self.get_article_request(article_slug)
        res_data = json.loads(res.data)
        adjacent_articles_meta = res_data['meta']['adjacent_articles']

        assert res.status_code == 200
        assert adjacent_articles_meta['prev']['title'] == prev_article_title
        assert adjacent_articles_meta['next']['title'] == next_article_title

    def test_first_article_meta_includes_next_but_not_prev_article(self) -> None:
        article_slug = generate_slug(articles[0]['title'])

        next_article_title = articles[1]['title']

        res = self.get_article_request(article_slug)
        res_data = json.loads(res.data)
        adjacent_articles_meta = res_data['meta']['adjacent_articles']

        assert res.status_code == 200
        assert adjacent_articles_meta['prev'] is None
        assert adjacent_articles_meta['next']['title'] == next_article_title

    def test_last_article_meta_includes_prev_but_not_next_article(self) -> None:
        article_slug = generate_slug(articles[-1]['title'])

        prev_article_title = articles[-2]['title']

        res = self.get_article_request(article_slug)
        res_data = json.loads(res.data)
        adjacent_articles_meta = res_data['meta']['adjacent_articles']

        assert res.status_code == 200
        assert adjacent_articles_meta['prev']['title'] == prev_article_title
        assert adjacent_articles_meta['next'] is None

    def test_cannot_get_article_for_non_existing_slug(self) -> None:
        non_existing_article_slug = 'this-article-does-not-exist'

        res = self.get_article_request(non_existing_article_slug)
        res_data = json.loads(res.data)

        assert res.status_code == 404
        assert res_data['error']['message'] == 'Article not found'
