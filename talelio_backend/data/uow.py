from types import TracebackType
from typing import Optional, Type, TypeVar

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from talelio_backend.core.db import default_session
from talelio_backend.data.repositories import AccountRepository

UnitOfWorkType = TypeVar('UnitOfWorkType', bound='UnitOfWork')


class UnitOfWork:
    session: Session
    account: AccountRepository

    def __init__(self, session_factory: sessionmaker = default_session) -> None:
        self.session_factory = session_factory

    def __enter__(self: UnitOfWorkType) -> UnitOfWorkType:
        self.session = self.session_factory()
        self.account = AccountRepository(self.session)

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        if exception_type is not None:
            self.session.rollback()

        self.session.close()

    def commit(self) -> None:
        self.session.commit()
