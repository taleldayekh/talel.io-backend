from typing import Any

from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import func

from talelio_backend.shared.data.repository import BaseRepository


class ArticleRepository(BaseRepository):

    def get(self, model: Any, **kwargs: Any) -> Any:
        if 'slug' in kwargs:
            query_res = self.session.query(model).filter_by(slug=kwargs.get('slug')).first()
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
