from typing import Any

from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import func

from talelio_backend.app_article.domain.article_model import Article
from talelio_backend.shared.data.repository import BaseRepository


class ArticleRepository(BaseRepository):

    def create(self, article: Article, user_id: int):
        SEARCH_QUERY = (f"""
            SELECT *
            FROM article
            WHERE slug LIKE %s;
            """)

        INSERT_QUERY = (f"""
            WITH created_article AS
            (
                INSERT INTO article 
                (
                    user_id,
                    title,
                    slug,
                    body, 
                    html,
                    meta_description,
                    table_of_contents,
                    featured_image,
                    url
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            )
            SELECT created_article.id,
                   created_article.created_at,
                   created_article.updated_at,
                   created_article.title,
                   created_article.slug,
                   created_article.body,
                   created_article.html,
                   created_article.meta_description,
                   created_article.table_of_contents,
                   created_article.featured_image,
                   created_article.url,
                   "user".id,
                   "user".username,
                   "user".location,
                   "user".avatar_url
            FROM created_article JOIN "user"
            ON created_article.user_id = "user".id;
            """)

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(SEARCH_QUERY, ('%' + article.slug + '%', ))

                conflicting_slug = len(cursor.fetchall())

                if conflicting_slug > 0:
                    article.slug = article.slug + '-' + str(conflicting_slug + 1)

                cursor.execute(INSERT_QUERY,
                               (user_id, article.title, article.slug, article.body, article.html,
                                article.meta_description, article.table_of_contents,
                                article.featured_image, article.url))

                return cursor.fetchone()

    def get_by_slug(self, slug: str):
        QUERY = (f"""
        """)

    def get_all_for_user(self, username: str, limit: int, offset: int):
        QUERY = (f"""
            SELECT article.id,
                   article.created_at,
                   article.updated_at,
                   article.title,
                   article.slug,
                   article.body,
                   article.html,
                   article.meta_description,
                   article.table_of_contents,
                   article.featured_image,
                   article.url,
                   "user".id,
                   "user".username,
                   "user".location,
                   "user".avatar_url,
                   COUNT(*) OVER() as total_articles_count
            FROM article
            JOIN "user" ON article.user_id = "user".id
            WHERE article.user_id = (
                SELECT id
                FROM "user"
                WHERE username = %s
                LIMIT 1
            )
            ORDER BY article.created_at DESC
            LIMIT %s
            OFFSET %s;
            """)

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(QUERY, (username, limit, offset))

                return cursor.fetchall()

    def get(self, model: Any, **kwargs: Any) -> Any:
        if not kwargs:
            query_res = self.session.query(model).order_by(model.id.desc()).first()

            return query_res
        if 'slug' in kwargs:
            # TODO: Improve querying to be more efficient instead of making multiple queries.
            slug = kwargs.get('slug')

            article_query_res = self.session.query(model).filter_by(slug=slug).first()

            if article_query_res is not None:
                next_article_query = self.session.query(model).with_entities(
                    model.title, model.slug)
                next_article_query = next_article_query.order_by(model.id.asc())
                next_article_query_res = next_article_query.where(
                    model.id > article_query_res.id).first()

                prev_article_query = self.session.query(model).with_entities(
                    model.title, model.slug)
                prev_article_query = prev_article_query.order_by(model.id.desc())
                prev_article_query_res = prev_article_query.where(
                    model.id < article_query_res.id).first()
            else:
                next_article_query_res = None
                prev_article_query_res = None

            return {
                'article': article_query_res,
                'next_article_meta': next_article_query_res,
                'prev_article_meta': prev_article_query_res
            }

        # TODO: Raise exception and return 404.
        return {}
