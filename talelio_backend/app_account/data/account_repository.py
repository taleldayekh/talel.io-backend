from typing import Any

from talelio_backend.shared.data.repository import BaseRepository


class AccountRepository(BaseRepository):

    def get(self, model: Any, **kwargs: Any) -> Any:
        account: Any

        if 'email' in kwargs:
            account = self.session.query(model).filter_by(email=kwargs.get('email')).first()

        return account
