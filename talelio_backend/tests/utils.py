from typing import Dict

from talelio_backend.identity_and_access.authentication import JWT
from talelio_backend.tests.constants import INITIAL_USER_ID, USERNAME_TALEL


def generate_authorization_header(user_id: int = INITIAL_USER_ID,
                                  username: str = USERNAME_TALEL,
                                  no_token: bool = False,
                                  invalid_token: bool = False) -> Dict[str, str]:
    access_token = JWT.generate_token({'user_id': user_id, 'username': username})

    if no_token:
        authorization_header = {'Authorization': 'Bearer '}
        return authorization_header

    if invalid_token:
        authorization_header = {'Authorization': f'Bearer {access_token + "1986"}'}
        return authorization_header

    authorization_header = {'Authorization': f'Bearer {access_token}'}

    return authorization_header
