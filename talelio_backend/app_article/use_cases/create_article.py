# pylint: disable=W0104
from typing import Dict, Union

from talelio_backend.app_article.domain.article_model import Article
from talelio_backend.data.uow import UnitOfWork


def create_article(uow: UnitOfWork, user_id: int, title: str, body: str, meta_description: str,
                   featured_image: str) -> Dict[str, Dict[str, Union[str, int]]]:
    with uow:
        article = Article(title, body, meta_description, featured_image)
        article.convert_body_to_html
        article.generate_table_of_contents

        article_record = uow.article.create(article, user_id)

        return {
            "article": {
                "id": article_record[0],
                "created_at": article_record[1],
                "updated_at": article_record[2],
                "title": article_record[3],
                "slug": article_record[4],
                "body": article_record[5],
                "html": article_record[6],
                "meta_description": article_record[7],
                "table_of_contents": article_record[8],
                "featured_image": article_record[9],
                "url": article_record[10],
            },
            "user": {
                "id": article_record[11],
                "username": article_record[12],
                "location": article_record[13],
                "avatar_url": article_record[14],
            }
        }


def create_paid_article():
    pass
