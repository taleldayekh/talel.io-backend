from typing import Tuple, cast

from flask import Blueprint, Response, request

from talelio_backend.app_social.use_cases.create_actor import create_actor
from talelio_backend.app_social.use_cases.discover import webfinger_discover
from talelio_backend.app_social.use_cases.get_actor import get_actor
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.identity_and_access.authentication import Authentication
from talelio_backend.identity_and_access.authorization import authorization_required
from talelio_backend.interfaces.api.errors import APIError
from talelio_backend.interfaces.api.socials.actor_serializer import SerializeActor
from talelio_backend.interfaces.api.socials.webfinger_serializer import SerializeWebFinger
from talelio_backend.interfaces.api.utils import extract_access_token_from_authorization_header
from talelio_backend.shared.exceptions import AuthorizationError, UserError

socials_v1 = Blueprint('socials_v1', __name__)


@socials_v1.get('/.well-known/webfinger')
def webfinger() -> Tuple[Response, int]:
    try:
        resource_query_param = request.args.get('resource')

        if not resource_query_param or not resource_query_param.startswith('acct:'):
            raise APIError('Invalid WebFinger request', 400)

        username = resource_query_param.split('acct:')[1].split('@')[0]
        uow = UnitOfWork()

        webfinger = webfinger_discover(uow, username)

        res_body = SerializeWebFinger().dump(webfinger)

        return res_body, 200
    except UserError as error:
        raise APIError(str(error), 404) from error


# TODO: Reiterate
@socials_v1.post('/actors')
def create_actor_endpoint() -> Tuple[Response, int]:
    authorization_header = request.headers.get('Authorization')

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

            # TODO: Return proper response
            return 'Hello World'
        except Exception as error:
            print(error)
            return 'Hello World'

    try:
        return protected_create_actor_endpoint()
    except AuthorizationError as error:
        raise APIError(str(error), 403) from error


@socials_v1.get('/actors/<string:username>')
def get_actor_endpoint(username: str) -> Tuple[Response, int]:
    try:
        uow = UnitOfWork()

        actor = get_actor(uow, username)

        res_body = SerializeActor().dump(actor)

        return res_body, 200
    except ValueError as error:
        raise APIError(str(error), 500) from error
    except UserError as error:
        raise APIError(str(error), 404) from error
