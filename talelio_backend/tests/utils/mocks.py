from os import getenv
from types import TracebackType
from typing import Any, Dict, Optional, Set, Type, TypeVar, Union, cast

from itsdangerous import TimedJSONWebSignatureSerializer

SECRET_KEY = cast(str, getenv('SECRET_KEY'))

FakeUnitOfWorkType = TypeVar('FakeUnitOfWorkType', bound='FakeUnitOfWork')


class FakeRepository:
    def __init__(self) -> None:
        self.fake_db: Set[Any] = set()

    def add(self, model: Any) -> None:
        self.fake_db.add(model)

    def get(self) -> None:
        pass


class FakeAccountRepository(FakeRepository):
    pass


class FakeUnitOfWork:
    account: FakeAccountRepository

    def __init__(self) -> None:
        self.committed = False

    def __enter__(self: FakeUnitOfWorkType) -> FakeUnitOfWorkType:
        self.account = FakeAccountRepository()
        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        pass

    def commit(self) -> None:
        self.committed = True


def generate_verification_token(expire_sec: Union[int, None], data: Dict) -> str:
    serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, expire_sec)
    token = serializer.dumps(data)

    return str(token, 'utf-8')
