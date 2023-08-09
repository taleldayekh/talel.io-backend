from __future__ import annotations

from types import TracebackType
from typing import Any, Optional, Type

from talelio_backend.app_account.data.account_repository import AccountRepository
from talelio_backend.app_article.data.article_repository import ArticleRepository
from talelio_backend.app_user.data.user_repository import UserRepository
from talelio_backend.libs.db_client import DbClient


class UnitOfWork:
    session: Any
    account: AccountRepository
    user: UserRepository
    article: ArticleRepository

    def __init__(self, db_client: DbClient = DbClient) -> None:
        self.db_client = db_client()

    def __enter__(self: UnitOfWork) -> UnitOfWork:
        self.session = self.db_client.get_connection
        self.account = AccountRepository(self.session)
        self.user = UserRepository(self.session)
        self.article = ArticleRepository(self.session)

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.session.close()
        print('Db connection closed')
