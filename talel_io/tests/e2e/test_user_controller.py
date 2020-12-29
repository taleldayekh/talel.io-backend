# pylint: disable=E1101, R0903
# mypy: ignore-errors
# import json

import pytest


@pytest.mark.usefixtures('api_server')
class TestUserGET:
    def test_get_user_returns_200(self) -> None:
        # res = self.api.get('api/v1/user/')
        res = self.api.get('/')

        assert res.status_code == 200
        # res_data = json.loads(res.get_data(as_text=True))

        # assert res_data['message'] == 'talel.io API'
        # assert res.status_code == 200
