from typing import Dict

import pytest
from flask import json

from talelio_backend.tests.e2e.helpers import RequestHelper
from talelio_backend.tests.mocks.projects import talelio_server_project
from talelio_backend.tests.utils import generate_authorization_header


@pytest.mark.usefixtures('populate_db_account')
class TestCreateProject(RequestHelper):

    def test_can_create_project(self, authorization_header: Dict[str, str]) -> None:
        res = self.create_project_request(authorization_header, talelio_server_project)
        res_data = json.loads(res.data)

        assert res.status_code == 201
        assert res_data['title'] == talelio_server_project['title']
        assert res_data['body'] == talelio_server_project['body']

    def test_cannot_create_project_when_missing_details(
            self, authorization_header: Dict[str, str]) -> None:
        res = self.create_project_request(authorization_header,
                                          {'title': talelio_server_project['title']})
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == "Expected 'body' key"

    def test_cannot_create_project_with_missing_request_body(
            self, authorization_header: Dict[str, str]) -> None:
        res = self.create_project_request(authorization_header)
        res_data = json.loads(res.data)

        assert res.status_code == 400
        assert res_data['error']['message'] == 'Missing request body'

    def test_cannot_create_project_for_unauthorized_user(self) -> None:
        res_no_authorization_header = self.create_project_request({}, talelio_server_project)
        res_no_authorization_header_data = json.loads(res_no_authorization_header.data)

        assert res_no_authorization_header.status_code == 403
        assert res_no_authorization_header_data['error'][
            'message'] == 'No authorization header provided'

        no_token_authorization_header = generate_authorization_header(no_token=True)
        res_no_token_authorization_header = self.create_project_request(
            no_token_authorization_header, talelio_server_project)
        res_no_token_authorization_header_data = json.loads(res_no_token_authorization_header.data)

        assert res_no_token_authorization_header.status_code == 403
        assert res_no_token_authorization_header_data['error'][
            'message'] == 'No authorization token provided'

        invalid_token_authorization_header = generate_authorization_header(invalid_token=True)
        res_invalid_token_authorization_header = self.create_project_request(
            invalid_token_authorization_header, talelio_server_project)

        assert res_invalid_token_authorization_header.status_code == 403
