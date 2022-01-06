from typing import Any

from sqlalchemy.orm.session import Session


class BaseRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, model: Any) -> Any:
        self.session.add(model)
        self.session.flush()

        return model
