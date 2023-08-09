from re import findall

import pytest
from flask import json

from talelio_backend.tests.constants import INVALID_USER, USERNAME_TALEL
from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.articles import fixed_or_rotary_wing_article, hiking_gear_article
from talelio_backend.tests.mocks.projects import talelio_client_project, talelio_server_project


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


# TODO: Uncomment when projects are implemented
# @pytest.mark.usefixtures('populate_db_account', 'populate_db_projects')
# class TestGetUserProjects(RequestHelper):

#     def test_can_get_user_projects(self) -> None:
#         res = self.get_user_projects_request(USERNAME_TALEL)
#         res_data = json.loads(res.data)

#         assert res.status_code == 200
#         assert len(res_data) == 2
#         assert res_data[0]['title'] == talelio_server_project['title']
#         assert res_data[1]['title'] == talelio_client_project['title']

#     def test_cannot_get_projects_for_non_existing_user(self) -> None:
#         res = self.get_user_projects_request(INVALID_USER)
#         res_data = json.loads(res.data)

#         assert res.status_code == 400
#         assert res_data['error']['message'] == f"User '{INVALID_USER}' does not exist"
