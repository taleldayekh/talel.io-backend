from __future__ import annotations

from types import TracebackType
from typing import Optional, Type, Union

from sqlalchemy.dialects.postgresql.dml import Insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from talelio_backend.app_account.data.account_repository import AccountRepository
from talelio_backend.app_article.data.article_repository import ArticleRepository
from talelio_backend.app_project.data.project_repository import ProjectRepository
from talelio_backend.app_user.data.user_repository import UserRepository
from talelio_backend.core.db import default_session


class UnitOfWork:
    session: Session
    account: AccountRepository
    user: UserRepository
    projects: ProjectRepository
    articles: ArticleRepository

    def __init__(self, session_factory: sessionmaker = default_session) -> None:
        self.session_factory = session_factory

    def __enter__(self: UnitOfWork) -> UnitOfWork:
        self.session = self.session_factory()
        self.account = AccountRepository(self.session)
        self.user = UserRepository(self.session)
        self.projects = ProjectRepository(self.session)
        self.articles = ArticleRepository(self.session)

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        if exception_type is not None:
            self.session.rollback()

        self.session.close()

    def commit(self, statement: Optional[Insert] = None) -> Union[Insert, None]:
        if statement is None:
            self.session.commit()

            return None

        result = self.session.execute(statement)

        return result
