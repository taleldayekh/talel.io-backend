from sqlalchemy.orm import sessionmaker

from talelio_backend.app_user.domain.user_model import User


class UserRepository:
    def __init__(self, session: sessionmaker) -> None:
        self.session = session

    def add(self, user: User) -> None:
        pass

    def get(self) -> None:
        pass
