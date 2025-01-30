from typing import Tuple, cast

from flask import Blueprint, Response, request

from talelio_backend.app_social.use_cases.create_actor import create_actor
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.identity_and_access.authentication import Authentication
from talelio_backend.identity_and_access.authorization import authorization_required
from talelio_backend.interfaces.api.errors import APIError
from talelio_backend.interfaces.api.utils import extract_access_token_from_authorization_header
from talelio_backend.shared.exceptions import AuthorizationError

socials_v1 = Blueprint('socials_v1', __name__)


@socials_v1.post('/actor')
def create_actor_endpoint() -> Tuple[Response, int]:
    authorization_header = request.header.get('Authorization')

    @authorization_required(authorization_header)
    def protected_create_actor_endpoint() -> Tuple[Response, int]:
        try:
            if not request.json:
                raise APIError('Missing request body', 400)

            access_token = extract_access_token_from_authorization_header(
                cast(str, authorization_header))
            user = Authentication().get_jwt_identity(access_token)

            user_id = int(user['user_id'])
            username = request.json['username']

            uow = UnitOfWork()

            created_actor = create_actor(uow, user_id, username)
        except:
            pass

    try:
        return protected_create_actor_endpoint()
    except AuthorizationError as error:
        raise APIError(str(error), 403) from error
