from os import getenv
from typing import Union

from redis import Redis

HOST = getenv('HOST') or 'localhost'

redis_client = Redis(host=HOST)


class TokenStore:

    def __init__(self, redis: Redis = redis_client) -> None:
        self.redis = redis

    def set_token(self, user_id: int, token: str, exp: int = 604800) -> None:
        self.redis.set(str(user_id), token, ex=exp)

    def get_token(self, user_id: int) -> Union[str, None]:
        token = self.redis.get(str(user_id))

        if token:
            return token.decode('utf-8')
        return None

    def delete_token(self, user_id: int) -> int:
        return self.redis.delete(str(user_id))
