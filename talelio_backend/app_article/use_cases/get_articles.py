from typing import Dict, Optional, Union

from talelio_backend.app_article.domain.article_model import Article
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.shared.utils.pagination import Pagination


def get_articles_for_user(
        uow: UnitOfWork, username: str, page: Optional[Union[int, None]],
        limit: Optional[Union[int, None]]) -> Union[Dict, Dict[str, Union[User, int, str, None]]]:
    with uow:
        page = page if page and page != 0 else 1
        limit = limit if limit and limit != 0 else 10

        offset = Pagination.calculate_offset(page, limit)

        user_articles_record = uow.articles.get(User,
                                                username=username,
                                                limit=limit,
                                                offset=offset)

        if len(user_articles_record) == 0:
            return {}

        user_articles_record = user_articles_record[0]._asdict()

        user = user_articles_record['User']
        total_articles_count = user_articles_record['total_articles_count']

        pages = Pagination.total_pages(total_articles_count, limit)
        last_page = page == pages

        next_link = (f'/users/{username}/articles?page={page + 1}&limit={limit}'
                     if not last_page else None)
        prev_link = (f'/users/{username}/articles?page={page - 1}&limit={limit}'
                     if page - 1 != 0 else None)

        return {
            'user': user,
            'total_articles_count': total_articles_count,
            'next_link': next_link,
            'prev_link': prev_link
        }


def get_article(uow: UnitOfWork, slug: str) -> Article:
    with uow:
        article_record = uow.articles.get(Article, slug=slug)

        return article_record
