from typing import Any

from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import func

from talelio_backend.shared.data.repository import BaseRepository


class UserRepository(BaseRepository):

    def get(self, model: Any, **kwargs: Any) -> Any:
        query: Any

        if 'id' in kwargs:
            query = self.session.query(model).filter_by(id=kwargs.get('id')).first()
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
            query = query.options(contains_eager(model.articles)).populate_existing().all()

        return query
