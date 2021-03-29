from typing import Any

from sqlalchemy.orm.session import Session


class BaseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, model: Any) -> Any:
        self.session.add(model)
        self.session.flush()

        return model

    def get(self, model: Any, **kwargs: Any) -> None:
        pass


class AccountRepository(BaseRepository):
    def get(self, model: Any, **kwargs: Any) -> Any:
        if 'email' in kwargs:
            return self.session.query(model).filter_by(email=kwargs.get('email')).first()
        return None


class UserRepository(BaseRepository):
    def get(self, model: Any, **kwargs: Any) -> Any:
        if 'username' in kwargs:
            return self.session.query(model).filter_by(username=kwargs.get('username')).first()
        return None


class ProjectRepository(BaseRepository):
    def get(self, model: Any, **kwargs: Any) -> Any:
        return self.session.query(model).order_by(model.id.desc()).first()
