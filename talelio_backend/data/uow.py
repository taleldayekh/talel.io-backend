from __future__ import annotations

from types import TracebackType
from typing import Any, Optional, Type

from talelio_backend.app_account.data.account_repository import AccountRepository
from talelio_backend.app_user.data.user_repository import UserRepository
from talelio_backend.libs.db_client import DbClient


class UnitOfWork:
    session: Any
    account: AccountRepository
    user: UserRepository

    def __init__(self, db_client: DbClient = DbClient) -> None:
        self.db_client = db_client()

    def __enter__(self: UnitOfWork) -> UnitOfWork:
        self.session = self.db_client.get_connection
        self.account = AccountRepository(self.session)
        self.user = UserRepository(self.session)

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.session.close()
        print('Db connection closed')


# from __future__ import annotations

# from types import TracebackType
# from typing import Optional, Type

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm.session import Session

# from talelio_backend.app_account.data.account_repository import AccountRepository
# from talelio_backend.app_article.data.article_repository import ArticleRepository
# from talelio_backend.app_project.data.project_repository import ProjectRepository
# from talelio_backend.app_user.data.user_repository import UserRepository
# from talelio_backend.core.db import default_session

# from talelio_backend.libs.db_client import DbClient

# class UnitOfWork:
#     db: DbClient
#     account: AccountRepository
#     # user: UserRepository
#     # projects: ProjectRepository
#     # articles: ArticleRepository

#     def __init__(self, db_client: DbClient = DbClient) -> None:
#         self.db_client = db_client

#     def __enter__(self: UnitOfWork) -> UnitOfWork:
#         self.db = self.db_client()
#         self.account = AccountRepository(self.db)
#         # self.user = UserRepository(self.db)
#         # self.projects = ProjectRepository(self.db)
#         # self.articles = ArticleRepository(self.db)

#         return self

#     def __exit__(self, exception_type: Optional[Type[BaseException]],
#                  exception_value: Optional[BaseException],
#                  traceback: Optional[TracebackType]) -> None:
#         ! Do I need to take this into consideration
#         if exception_type is not None:
#             self.db.rollback()

#         self.db.close()

#     # TODO: Delete these methods
#     def flush(self) -> None:
#         self.db.flush()

#     def commit(self) -> None:
#         self.db.commit()
