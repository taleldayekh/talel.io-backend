import hashlib
import string
from random import choice
from typing import Any, Dict, Union

from jwt import decode, encode

from talelio_backend.shared.constants import SECRET_KEY


class JWT:
    @staticmethod
    def generate_token(payload: Dict[str, Any], secret_key: str = SECRET_KEY) -> str:
        return encode(payload, secret_key, algorithm='HS512')

    @staticmethod
    def verify_token(token: str, secret_key: str = SECRET_KEY) -> Dict[str, str]:
        return decode(token, secret_key, algorithms=['HS512'])

    def get_jwt_identity(self, token: str) -> Dict[str, str]:
        return self.verify_token(token)


def generate_salt() -> str:
    return ''.join([choice(string.ascii_letters) for ascii_letter in range(5)])


def generate_password_hash(password: str, salt: Union[None, str] = None) -> str:
    if not salt:
        salt = generate_salt()

    password_hash = hashlib.sha3_512(str.encode(password + salt)).hexdigest()

    return f'{password_hash},{salt}'


def check_password_hash(password: str, password_hash: str) -> bool:
    salt = password_hash.split(',')[1]

    return bool(generate_password_hash(password, salt) == password_hash)
