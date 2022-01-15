# pylint: disable=W0104
from talelio_backend.app_article.domain.article_model import Article
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.exceptions import UserError
from talelio_backend.data.uow import UnitOfWork


def create_article(uow: UnitOfWork, user_id: int, title: str, body: str) -> Article:
    with uow:
        user_record = uow.user.get(User, id=user_id)

        if user_record is None:
            raise UserError('User does not exist')

        new_article = Article(title, body)
        new_article.convert_body_to_html

        user_record.articles.append(new_article)
        uow.commit()

        article_record = uow.articles.get(Article)

        return article_record
