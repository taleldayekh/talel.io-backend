from typing import Tuple

from flask import Blueprint, request
from itsdangerous import SignatureExpired

from talelio_backend.app_account.use_cases.register_account import (register_account,
                                                                    send_registration_email)
from talelio_backend.interfaces.api.errors import APIError

account_v1 = Blueprint('account_v1', __name__)


@account_v1.route('/register', methods=['POST'])
def registration_email_endpoint() -> Tuple[str, int]:
    try:
        email = request.json['email']
        password = request.json['password']

        send_registration_email(email, password)

        return 'Success Message', 200
    except KeyError as error:
        raise APIError(f'Expected {error} key', 400) from error


@account_v1.route('/register/<string:token>', methods=['GET'])
def register_account_endpoint(token: str) -> Tuple[str, int]:
    try:
        register_account(token)

        return 'Success Message', 200
    except SignatureExpired as error:
        raise APIError(str(error), 400) from error
