from functools import wraps
from typing import Any, Union

from talelio_backend.core.exceptions import AuthorizationError
from talelio_backend.identity_and_access.authentication import verify_access_token


def authorization_required(authorization_header: Union[str, None]) -> Any:
    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not authorization_header:
                raise AuthorizationError('No authorization header provided')

            access_token = authorization_header.split(' ')[1]

            if not access_token:
                raise AuthorizationError('No authorization token provided')

            try:
                verify_access_token(access_token)
            except Exception as e:
                raise AuthorizationError(e) from e

            return func(*args, **kwargs)

        return wrapper

    return decorator
