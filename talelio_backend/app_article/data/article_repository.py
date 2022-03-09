from typing import Any

from talelio_backend.shared.data.repository import BaseRepository


class ArticleRepository(BaseRepository):

    def get(self, model: Any, **kwargs: Any) -> Any:
        if 'slug' in kwargs:
            return self.session.query(model).filter_by(slug=kwargs.get('slug')).first()

        return self.session.query(model).order_by(model.id.desc()).first()
