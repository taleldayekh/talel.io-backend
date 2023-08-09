# TODO: Uncomment when projects are implemented
# from typing import Tuple, cast

# from flask import Blueprint, Response, request

# from talelio_backend.app_project.use_cases.create_project import create_project
# from talelio_backend.core.exceptions import AuthorizationError
# from talelio_backend.data.uow import UnitOfWork
# from talelio_backend.identity_and_access.authentication import Authentication
# from talelio_backend.identity_and_access.authorization import authorization_required
# from talelio_backend.interfaces.api.errors import APIError
# from talelio_backend.interfaces.api.projects.project_serializer import ProjectSchema
# from talelio_backend.interfaces.api.utils import extract_access_token_from_authorization_header

# projects_v1 = Blueprint('projects_v1', __name__)

# @projects_v1.post('')
# def create_project_endpoint() -> Tuple[Response, int]:
#     authorization_header = request.headers.get('Authorization')

#     @authorization_required(authorization_header)
#     def protected_create_project_endpoint() -> Tuple[Response, int]:
#         try:
#             if not request.json:
#                 raise APIError('Missing request body', 400)

#             access_token = extract_access_token_from_authorization_header(
#                 cast(str, authorization_header))
#             uow = UnitOfWork()

#             user = Authentication().get_jwt_identity(access_token)
#             user_id = int(user['user_id'])
#             title = request.json['title']
#             body = request.json['body']

#             created_project = create_project(uow, user_id, title, body)
#             res_body = ProjectSchema().dump(created_project)

#             return res_body, 201
#         except KeyError as error:
#             raise APIError(f'Expected {error} key', 400) from error

#     try:
#         return protected_create_project_endpoint()
#     except AuthorizationError as error:
#         raise APIError(str(error), 403) from error
