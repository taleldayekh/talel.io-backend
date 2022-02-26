# pylint: disable=W0104
from typing import Optional

# TODO: Wrap in custom DbIntegrityError exception class
from sqlalchemy.exc import IntegrityError

from talelio_backend.app_article.domain.article_model import Article
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.exceptions import UserError
from talelio_backend.data.uow import UnitOfWork


def create_article(uow: UnitOfWork, user_id: int, title: str, body: str) -> Article:

    def new_article(conflicting_slug: Optional[bool] = False) -> None:
        with uow:
            user_record = uow.user.get(User, id=user_id)

            if user_record is None:
                raise UserError('User does not exist')

            new_article = Article(title, body)
            new_article.convert_body_to_html

            if conflicting_slug:
                new_article.slug = new_article.slug + '-'

            user_record.articles.append(new_article)

            if conflicting_slug:
                uow.flush()

                article_id = sorted(user_record.articles,
                                    key=lambda article: article.id,
                                    reverse=True)[0].id

                updated_slug = f'{new_article.slug}{str(article_id)}'
                new_article.slug = updated_slug

                user_record.articles.append(new_article)

            try:
                uow.commit()
            except IntegrityError as error:
                raise error

    try:
        new_article()
    except IntegrityError:
        new_article(True)
    finally:
        with uow:
            article_record = uow.articles.get(Article)

    return article_record
