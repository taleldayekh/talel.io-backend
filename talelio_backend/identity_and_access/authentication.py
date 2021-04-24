from typing import Dict

from jwt import decode, encode

from talelio_backend.constants import SECRET_KEY


def generate_access_token(payload: Dict[str, str]) -> str:
    return encode(payload, SECRET_KEY, algorithm='HS512')


def verify_access_token(token: str) -> Dict[str, str]:
    return decode(token, SECRET_KEY, algorithms=['HS512'])
