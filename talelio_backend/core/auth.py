import hashlib
import string
from random import choice
from typing import Union


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
