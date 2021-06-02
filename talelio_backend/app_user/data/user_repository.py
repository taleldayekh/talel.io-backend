from typing import Any

from talelio_backend.shared.data.repository import BaseRepository


class UserRepository(BaseRepository):
    def get(self, model: Any, **kwargs: Any) -> Any:
        user: Any

        if 'id' in kwargs:
            user = self.session.query(model).filter_by(id=kwargs.get('id')).first()
        if 'username' in kwargs:
            user = self.session.query(model).filter_by(username=kwargs.get('username')).first()

        return user
