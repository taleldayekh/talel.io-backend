from typing import Dict

import pytest
from flask import json

from talelio_backend.tests.constants import INVALID_USER, USERNAME_TALEL
from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.projects import talelio_client_project, talelio_server_project
from talelio_backend.tests.utils import generate_authorization_header


@pytest.mark.usefixtures('populate_db_account')
class TestCreateUserProject(RequestHelper):
    def test_can_create_user_project(self, authorization_header: Dict[str, str]) -> None:
        res = self.create_user_project_request(USERNAME_TALEL, talelio_server_project,
                                               authorization_header)
        res_data = json.loads(res.data)

        assert res.status_code == 201
        assert res_data['title'] == talelio_server_project['title']
        assert res_data['body'] == talelio_server_project['body']

    def test_cannot_create_user_project_when_missing_project_details(
            self, authorization_header: Dict[str, str]) -> None:
        res = self.create_user_project_request(USERNAME_TALEL,
                                               {'title': talelio_server_project['title']},
                                               authorization_header)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == "Expected 'body' key"

    def test_cannot_create_user_project_for_non_existing_user(
            self, authorization_header: Dict[str, str]) -> None:
        res = self.create_user_project_request(INVALID_USER, talelio_server_project,
                                               authorization_header)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == f"User '{INVALID_USER}' does not exist"

    def test_cannot_create_user_project_for_unauthorized_user(self) -> None:
        res_no_authorization_header = self.create_user_project_request(
            USERNAME_TALEL, talelio_server_project, {})
        res_no_authorization_header_data = json.loads(res_no_authorization_header.data)

        assert res_no_authorization_header.status_code == 403
        assert res_no_authorization_header_data['error'][
            'message'] == 'No authorization header provided'

        no_token_authorization_header = generate_authorization_header(no_token=True)
        res_no_token_authorization_header = self.create_user_project_request(
            USERNAME_TALEL, talelio_server_project, no_token_authorization_header)
        res_no_token_authorization_header_data = json.loads(res_no_token_authorization_header.data)

        assert res_no_token_authorization_header.status_code == 403
        assert res_no_token_authorization_header_data['error'][
            'message'] == 'No authorization token provided'

        invalid_token_authorization_header = generate_authorization_header(invalid_token=True)
        res_invalid_token_authorization_header = self.create_user_project_request(
            USERNAME_TALEL, talelio_server_project, invalid_token_authorization_header)

        assert res_invalid_token_authorization_header.status_code == 403


@pytest.mark.usefixtures('populate_db_account', 'populate_db_project')
class TestGetUserProjects(RequestHelper):
    def test_can_get_user_projects(self, authorization_header: Dict[str, str]) -> None:
        res_one_project = self.get_user_projects_request(USERNAME_TALEL)
        res_one_project_data = json.loads(res_one_project.data)

        assert res_one_project.status_code == 200
        assert len(res_one_project_data) == 1
        assert res_one_project_data[0]['title'] == talelio_server_project['title']

        self.create_user_project_request(USERNAME_TALEL, talelio_client_project,
                                         authorization_header)

        res_two_projects = self.get_user_projects_request(USERNAME_TALEL)
        res_two_projects_data = json.loads(res_two_projects.data)

        assert len(res_two_projects_data) == 2

    def test_cannot_get_projects_for_non_existing_user(self) -> None:
        res = self.get_user_projects_request(INVALID_USER)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == f"User '{INVALID_USER}' does not exist"
