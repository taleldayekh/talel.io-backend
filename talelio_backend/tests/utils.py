from typing import Dict

from itsdangerous import TimedJSONWebSignatureSerializer

from talelio_backend.constants import SECRET_KEY
from talelio_backend.identity_and_access.authentication import generate_access_token
from talelio_backend.tests.constants import INITIAL_USER_ID, USERNAME_TALEL


def generate_verification_token(data: Dict[str, str], secret_key: str = SECRET_KEY) -> str:
    serializer = TimedJSONWebSignatureSerializer(secret_key)
    token = serializer.dumps(data)

    return str(token, 'utf-8')


def generate_authorization_header(user_id: int = INITIAL_USER_ID,
                                  username: str = USERNAME_TALEL,
                                  no_token: bool = False,
                                  invalid_token: bool = False) -> Dict[str, str]:
    access_token = generate_access_token({'user_id': user_id, 'username': username})

    if no_token:
        authorization_header = {'Authorization': 'Bearer '}
        return authorization_header

    if invalid_token:
        authorization_header = {'Authorization': f'Bearer {access_token + "1986"}'}
        return authorization_header

    authorization_header = {'Authorization': f'Bearer {access_token}'}

    return authorization_header
