from typing import Tuple, cast

from flask import Blueprint, request

from talelio_backend.app_project.use_cases.create_project import create_project
from talelio_backend.core.exceptions import AuthorizationError
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.identity_and_access.authentication import get_jwt_identity
from talelio_backend.identity_and_access.authorization import authorization_required
from talelio_backend.interfaces.api.errors import APIError
from talelio_backend.interfaces.api.projects.project_serializer import ProjectSchema

projects_v1 = Blueprint('projects_v1', __name__)


@projects_v1.route('', methods=['POST'])
def create_project_endpoint() -> Tuple[str, int]:
    authorization_header = request.headers.get('Authorization')

    @authorization_required(authorization_header)
    def protected() -> Tuple[str, int]:
        access_token = cast(str, authorization_header).split(' ')[1]
        user = get_jwt_identity(access_token)

        try:
            uow = UnitOfWork()

            title = request.json['title']
            body = request.json['body']

            user_id = int(user['user_id'])

            created_project = create_project(uow, user_id, title, body)
            res_body = ProjectSchema().dump(created_project)

            return res_body, 201
        except KeyError as error:
            raise APIError(f'Expected {error} key', 400) from error

    try:
        return protected()
    except AuthorizationError as error:
        raise APIError(str(error), 403) from error
