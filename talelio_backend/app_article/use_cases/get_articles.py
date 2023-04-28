from typing import Dict, Optional, Union, cast

from talelio_backend.app_article.domain.article_model import Article
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.exceptions import ArticleError
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
        prev_link = (f'/users/{username}/articles?page={page - 1}&limit={limit}' if page -
                     1 != 0 else None)

        return {
            'user': user,
            'total_articles_count': total_articles_count,
            'next_link': next_link,
            'prev_link': prev_link
        }


def get_article(uow: UnitOfWork, slug: str) -> Dict[str, Union[Article, Union[Dict, str, None]]]:
    with uow:
        article_record = uow.articles.get(Article, slug=slug)

        article = cast(Union[Article, None], article_record['article'])
        next_article_meta = article_record['next_article_meta']
        prev_article_meta = article_record['prev_article_meta']

        if article is None:
            raise ArticleError('Article not found')

        if next_article_meta is not None:
            next_article = {'title': next_article_meta[0], 'slug': next_article_meta[1]}
        else:
            next_article = None

        if prev_article_meta is not None:
            prev_article = {'title': prev_article_meta[0], 'slug': prev_article_meta[1]}
        else:
            prev_article = None

        adjacent_articles = {'next': next_article, 'prev': prev_article}

        return {'article': article, 'adjacent_articles': adjacent_articles}
