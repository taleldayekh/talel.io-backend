from typing import Any

from sqlalchemy.orm.session import Session


class BaseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, *args: Any) -> None:
        if len(args) == 1:
            model = args[0]
            self.session.add(model)

    def get(self) -> None:
        pass


class AccountRepository(BaseRepository):
    pass