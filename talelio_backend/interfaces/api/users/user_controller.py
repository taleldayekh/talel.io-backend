from typing import Tuple

from flask import Blueprint, jsonify, request

from talelio_backend.app_user.use_cases.create_user_project import create_user_project
from talelio_backend.app_user.use_cases.get_user_projects import get_user_projects
from talelio_backend.core.exceptions import UserError
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.interfaces.api.errors import APIError
from talelio_backend.interfaces.api.projects.project_serializer import ProjectSchema

users_v1 = Blueprint('users_v1', __name__)


@users_v1.route('/<string:username>/projects', methods=['GET'])
def get_user_projects_endpoint(username: str) -> Tuple[str, int]:
    try:
        uow = UnitOfWork()

        user_projects = get_user_projects(uow, username)
        res_body = ProjectSchema(many=True).dump(user_projects)

        return jsonify(res_body), 200
    except UserError as error:
        raise APIError(str(error), 400) from error


@users_v1.route('/<string:username>/projects', methods=['POST'])
def create_user_project_endpoint(username: str) -> Tuple[str, int]:
    try:
        uow = UnitOfWork()

        title = request.json['title']
        body = request.json['body']

        created_project = create_user_project(uow, username, title, body)
        res_body = ProjectSchema().dump(created_project)

        return res_body, 201
    except KeyError as error:
        raise APIError(f'Expected {error} key', 400) from error
    except UserError as error:
        raise APIError(str(error), 400) from error
