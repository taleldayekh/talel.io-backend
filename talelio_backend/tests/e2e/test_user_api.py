import pytest
from flask import json

from talelio_backend.tests.constants import INVALID_USER, USERNAME_TALEL
from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.articles import article_one, article_two
from talelio_backend.tests.mocks.projects import talelio_client_project, talelio_server_project


@pytest.mark.usefixtures('populate_db_account', 'populate_db_articles')
class TestGetUserArticles(RequestHelper):

    def test_can_get_user_articles(self) -> None:
        res = self.get_user_articles_request(USERNAME_TALEL)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert len(res_data) == 2
        assert res_data[0]['title'] == article_one['title']
        assert res_data[1]['title'] == article_two['title']

    def test_cannot_get_articles_for_non_existing_user(self) -> None:
        res = self.get_user_articles_request(INVALID_USER)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == f"User '{INVALID_USER}' does not exist"


@pytest.mark.usefixtures('populate_db_account', 'populate_db_projects')
class TestGetUserProjects(RequestHelper):

    def test_can_get_user_projects(self) -> None:
        res = self.get_user_projects_request(USERNAME_TALEL)
        res_data = json.loads(res.data)

        assert res.status_code == 200
        assert len(res_data) == 2
        assert res_data[0]['title'] == talelio_server_project['title']
        assert res_data[1]['title'] == talelio_client_project['title']

    def test_cannot_get_projects_for_non_existing_user(self) -> None:
        res = self.get_user_projects_request(INVALID_USER)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == f"User '{INVALID_USER}' does not exist"
