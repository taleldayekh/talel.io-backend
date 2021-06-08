from typing import Dict

import pytest
from flask import json

from talelio_backend.tests.constants import INVALID_USER, USERNAME_TALEL
from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.projects import talelio_client_project, talelio_server_project


@pytest.mark.usefixtures('populate_db_account', 'populate_db_project')
class TestGetUserProjects(RequestHelper):
    def test_can_get_user_projects(self, authorization_header: Dict[str, str]) -> None:
        res_one_project = self.get_user_projects_request(USERNAME_TALEL)
        res_one_project_data = json.loads(res_one_project.data)

        assert res_one_project.status_code == 200
        assert len(res_one_project_data) == 1
        assert res_one_project_data[0]['title'] == talelio_server_project['title']

        self.create_project_request(authorization_header, talelio_client_project)

        res_two_projects = self.get_user_projects_request(USERNAME_TALEL)
        res_two_projects_data = json.loads(res_two_projects.data)

        assert len(res_two_projects_data) == 2

    def test_cannot_get_projects_for_non_existing_user(self) -> None:
        res = self.get_user_projects_request(INVALID_USER)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == f"User '{INVALID_USER}' does not exist"
