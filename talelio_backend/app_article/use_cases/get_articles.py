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

        articles_record = uow.article.get_all_for_user(username, limit, offset)

        if not len(articles_record):
            return {}

        total_articles_count = articles_record[0][15]

        pages = Pagination.total_pages(total_articles_count, limit)
        last_page = page == pages

        next_link = (f'/users/{username}/articles?page={page + 1}&limit={limit}'
                     if not last_page else None)
        prev_link = (f'/users/{username}/articles?page={page - 1}&limit={limit}' if page -
                     1 != 0 else None)

        articles = [{
            'id': article_record[0],
            'created_at': article_record[1],
            'updated_at': article_record[2],
            'title': article_record[3],
            'slug': article_record[4],
            'body': article_record[5],
            'html': article_record[6],
            'meta_description': article_record[7],
            'table_of_contents': article_record[8],
            'featured_image': article_record[9],
            'url': article_record[10],
        } for article_record in articles_record]

        user = {
            'id': articles_record[0][11],
            'username': articles_record[0][12],
            'location': articles_record[0][13],
            'avatar_url': articles_record[0][14],
        }

        return {
            'articles': articles,
            'user': user,
            'total_articles_count': total_articles_count,
            'next_link': next_link,
            'prev_link': prev_link
        }


def get_article(uow: UnitOfWork, slug: str) -> Dict[str, Union[Article, Union[Dict, str, None]]]:
    with uow:
        article_record = uow.article.get_by_slug(slug)

        if article_record is None:
            raise ArticleError('Article not found')

        article = {
            'id': article_record[0],
            'created_at': article_record[1],
            'updated_at': article_record[2],
            'title': article_record[3],
            'slug': article_record[4],
            'body': article_record[5],
            'html': article_record[6],
            'meta_description': article_record[7],
            'table_of_contents': article_record[8],
            'featured_image': article_record[9],
            'url': article_record[10],
        }

        user = {
            'id': article_record[11],
            'username': article_record[12],
            'location': article_record[13],
            'avatar_url': article_record[14],
        }

        prev_article_title = article_record[15]
        prev_article_slug = article_record[16]
        next_article_title = article_record[17]
        next_article_slug = article_record[18]

        if prev_article_title is not None:
            prev_article = {'title': prev_article_title, 'slug': prev_article_slug}
        else:
            prev_article = None

        if next_article_title is not None:
            next_article = {'title': next_article_title, 'slug': next_article_slug}
        else:
            next_article = None

        adjacent_articles = {'next': next_article, 'prev': prev_article}

        return {'adjacent_articles': adjacent_articles, 'article': article, 'user': user}
