from typing import List

from talelio_backend.app_article.domain.article_model import Article
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.exceptions import UserError
from talelio_backend.data.uow import UnitOfWork


def get_user_articles(uow: UnitOfWork, username: str) -> List[Article]:
    with uow:
        user_record = uow.user.get(User, username=username)

        if user_record is None:
            raise UserError(f"User '{username}' does not exist")

        return user_record.articles
