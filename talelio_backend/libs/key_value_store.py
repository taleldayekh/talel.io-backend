import pickle
from os import getenv

from redis import Redis

HOST = getenv('HOST') or 'localhost'

redis_client = Redis(host=HOST)


class KeyValueStore:

    def __init__(self, redis: Redis = redis_client) -> None:
        self.redis = redis

    def set_string(self, key: str, value: str, ex: int = None) -> None:
        self.redis.set(key, value, ex=ex)

    def get_string(self, key: str) -> str | None:
        value = self.redis.get(key)

        return value.decode('utf-8') if value else None

    def set_data(self, key: str, value: object, ex: int = None) -> None:
        self.redis.set(key, pickle.dumps(value), ex=ex)

    def get_data(self, key: str) -> object | None:
        value = self.redis.get(key)

        return pickle.loads(value) if value else None
