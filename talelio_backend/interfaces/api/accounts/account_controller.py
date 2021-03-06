from typing import Tuple

from flask import Blueprint, jsonify, request
from itsdangerous import BadSignature

from talelio_backend.app_account.use_cases.register_account import register_account, verify_account
from talelio_backend.app_user.use_cases.authenticate_user import get_access_token
from talelio_backend.core.exceptions import (AccountError, AccountRegistrationError,
                                             AccountVerificationError)
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.interfaces.api.accounts.account_serializers import AccountSchema
from talelio_backend.interfaces.api.errors import APIError

accounts_v1 = Blueprint('accounts_v1', __name__)


@accounts_v1.route('/register', methods=['POST'])
def register_account_endpoint() -> Tuple[str, int]:
    try:
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


@accounts_v1.route('/verify/<string:token>', methods=['GET'])
def verify_account_endpoint(token: str) -> Tuple[str, int]:
    try:
        uow = UnitOfWork()

        verified_account = verify_account(uow, token)
        res_body = AccountSchema().dump(verified_account)

        return res_body, 200
    except BadSignature as error:
        raise APIError(str(error), 400) from error
    except AccountError as error:
        raise APIError(str(error), 400) from error
    except AccountVerificationError as error:
        raise APIError(str(error), 400) from error


@accounts_v1.route('/login', methods=['POST'])
def login_endpoint() -> Tuple[str, int]:
    try:
        uow = UnitOfWork()

        email = request.json['email']
        password = request.json['password']

        access_token = get_access_token(uow, email, password)

        return jsonify(access_token), 200
    except KeyError as error:
        raise APIError(f'Expected {error} key', 400) from error
    except AccountError as error:
        raise APIError(str(error), 401) from error
