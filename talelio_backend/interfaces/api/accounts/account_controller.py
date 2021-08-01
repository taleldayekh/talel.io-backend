from typing import Tuple

from flask import Blueprint, Response, jsonify, request
from jwt import InvalidSignatureError

from talelio_backend.app_account.use_cases.register_account import register_account, verify_account
from talelio_backend.app_user.use_cases.authenticate_user import (generate_access_token,
                                                                  get_access_token,
                                                                  set_refresh_token,
                                                                  verify_refresh_token)
from talelio_backend.core.exceptions import (AccountError, AccountRegistrationError,
                                             AccountVerificationError, TokenError)
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.identity_and_access.authentication import Authentication
from talelio_backend.identity_and_access.token_store import TokenStore
from talelio_backend.interfaces.api.accounts.account_serializers import AccountSchema
from talelio_backend.interfaces.api.errors import APIError

accounts_v1 = Blueprint('accounts_v1', __name__)


@accounts_v1.post('/register')
def register_account_endpoint() -> Tuple[Response, int]:
    try:
        if not request.json:
            raise APIError('Missing request body', 400)

        uow = UnitOfWork()

        email = request.json['email']
        password = request.json['password']
        username = request.json['username']

        registered_account = register_account(uow, email, password, username)
        res_body = AccountSchema().dump(registered_account)

        return res_body, 201
    except KeyError as error:
        raise APIError(f'Expected {error} key', 400) from error
    except AccountRegistrationError as error:
        raise APIError(str(error), 400) from error


@accounts_v1.get('/verify/<string:token>')
def verify_account_endpoint(token: str) -> Tuple[Response, int]:
    try:
        uow = UnitOfWork()

        verified_account = verify_account(uow, token)
        res_body = AccountSchema().dump(verified_account)

        return res_body, 200
    except InvalidSignatureError as error:
        raise APIError(str(error), 400) from error
    except AccountError as error:
        raise APIError(str(error), 400) from error
    except AccountVerificationError as error:
        raise APIError(str(error), 400) from error


@accounts_v1.post('/login')
def login_endpoint() -> Tuple[Response, int]:
    try:
        if not request.json:
            raise APIError('Missing request body', 400)

        uow = UnitOfWork()

        email = request.json['email']
        password = request.json['password']

        access_token = get_access_token(uow, email, password)

        user = Authentication().get_jwt_identity(access_token)
        user_id = int(user['user_id'])
        username = user['username']

        token_store = TokenStore()

        refresh_token = set_refresh_token(token_store, user_id, username)

        return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
    except KeyError as error:
        raise APIError(f'Expected {error} key', 400) from error
    except AccountError as error:
        raise APIError(str(error), 401) from error


@accounts_v1.post('/token')
def new_access_token_endpoint() -> Tuple[Response, int]:
    try:
        if not request.json:
            raise APIError('Missing request body', 400)

        refresh_token = request.json['refresh_token']

        user = Authentication().get_jwt_identity(refresh_token)
        user_id = int(user['user_id'])
        username = user['username']

        token_store = TokenStore()

        verify_refresh_token(token_store, user_id, refresh_token)
        access_token = generate_access_token(user_id, username)

        return jsonify({'access_token': access_token}), 200
    except KeyError as error:
        raise APIError(f'Expected {error} key', 400) from error
    except TokenError as error:
        raise APIError(str(error), 401) from error
