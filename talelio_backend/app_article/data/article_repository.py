from typing import Any

from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import func

from talelio_backend.shared.data.repository import BaseRepository


class ArticleRepository(BaseRepository):

    def get(self, model: Any, **kwargs: Any) -> Any:
        if 'slug' in kwargs:
            # TODO: Improve querying to be more efficient instead of making multiple queries.
            slug = kwargs.get('slug')

            article_query_res = self.session.query(model).filter_by(slug=slug).first()

            if article_query_res is not None:
                next_article_query = self.session.query(model).with_entities(model.title, model.slug)
                next_article_query = next_article_query.order_by(model.id.asc())
                next_article_query_res = next_article_query.where(
                    model.id > article_query_res.id).first()

                prev_article_query = self.session.query(model).with_entities(model.title, model.slug)
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
        if 'username' in kwargs:
            username = kwargs.get('username')
            limit = kwargs.get('limit')
            offset = kwargs.get('offset')

            query = self.session.query(
                model,
                func.count(model.articles).over().label('total_articles_count'))
            query = query.filter_by(username=username)
            query = query.join(model.articles).order_by(text('article.created_at desc'))
            query = query.limit(limit).offset(offset)
            query_res = query.options(contains_eager(model.articles)).populate_existing().all()
        else:
            query_res = self.session.query(model).order_by(model.id.desc()).first()

        return query_res
