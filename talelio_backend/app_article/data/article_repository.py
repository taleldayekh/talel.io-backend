from typing import Any, List

from talelio_backend.app_article.domain.article_model import Article
from talelio_backend.data.repository import BaseRepository


class ArticleRepository(BaseRepository):

    def create(self, article: Article, user_id: int) -> tuple[Any, ...]:
        search_query = """
            SELECT *
            FROM article
            WHERE slug LIKE %s;
            """

        insert_query = """
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
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(search_query, ('%' + article.slug + '%', ))

                conflicting_slug = len(cursor.fetchall())

                if conflicting_slug > 0:
                    article.slug = article.slug + '-' + str(conflicting_slug + 1)

                cursor.execute(insert_query,
                               (user_id, article.title, article.slug, article.body, article.html,
                                article.meta_description, article.table_of_contents,
                                article.featured_image, article.url))

                return cursor.fetchone()

    def get_by_slug(self, slug: str) -> tuple[Any, ...]:
        query = """
            WITH selected_article AS
                (
                    SELECT 
                           article.id,
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
                           LAG(title) OVER(ORDER BY article.created_at) as prev_title,
                           LAG(slug) OVER(ORDER BY article.created_at) as prev_slug,
                           LEAD(title) OVER(ORDER BY article.created_at) as next_title,
                           LEAD(slug) OVER(ORDER BY article.created_at) as next_slug
                    FROM article
                    JOIN "user" ON user_id = "user".id
                )
            SELECT *
            FROM selected_article
            WHERE slug = %s;
        """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (slug, ))

                return cursor.fetchone()

    def get_all_for_user(self, username: str, limit: int, offset: int) -> List[tuple[Any, ...]]:
        query = """
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
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (username, limit, offset))

                return cursor.fetchall()
