from typing import Any, Dict, Union

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects.postgresql.dml import Insert
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import cast

from talelio_backend.shared.data.orm import article_table
from talelio_backend.shared.data.repository import BaseRepository


class ArticleRepository(BaseRepository):

    def add(self, model: Any, **kwargs: Dict[str, Union[str, int]]) -> Insert:
        timestamp = {'created_at': func.now()}
        values = {**timestamp, **kwargs}

        statement = insert(model).values(values).returning(article_table)
        statement = statement.on_conflict_do_update(
            index_elements=[article_table.c.slug],
            set_={"slug": article_table.c.slug + '-' + cast(article_table.c.id, String)})

        return statement

    def get(self, model: Any) -> Any:
        return self.session.query(model).order_by(model.id.desc()).first()
