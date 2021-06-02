from typing import Any

from talelio_backend.shared.data.repository import BaseRepository


class ProjectRepository(BaseRepository):
    def get(self, model: Any) -> Any:
        return self.session.query(model).order_by(model.id.desc()).first()
