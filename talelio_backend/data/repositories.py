from typing import Any

from sqlalchemy.orm.session import Session


class BaseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, model: Any) -> Any:
        self.session.add(model)
        self.session.flush()

        return model


class AccountRepository(BaseRepository):
    def get(self, model: Any, **kwargs: Any) -> Any:
        account: Any

        if 'email' in kwargs:
            account = self.session.query(model).filter_by(email=kwargs.get('email')).first()

        return account


class UserRepository(BaseRepository):
    def get(self, model: Any, **kwargs: Any) -> Any:
        user: Any

        if 'id' in kwargs:
            user = self.session.query(model).filter_by(id=kwargs.get('id')).first()
        if 'username' in kwargs:
            user = self.session.query(model).filter_by(username=kwargs.get('username')).first()

        return user


class ProjectRepository(BaseRepository):
    def get(self, model: Any) -> Any:
        return self.session.query(model).order_by(model.id.desc()).first()
