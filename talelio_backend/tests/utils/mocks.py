from os import getenv
from typing import Dict, cast

from itsdangerous import TimedJSONWebSignatureSerializer

SECRET_KEY = cast(str, getenv('SECRET_KEY'))

def generate_verification_token(data: Dict[str, str], secret_key: str = SECRET_KEY) -> str:
    serializer = TimedJSONWebSignatureSerializer(secret_key)
    token = serializer.dumps(data)

    return str(token, 'utf-8')
