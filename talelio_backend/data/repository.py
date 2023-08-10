from typing import Any


class BaseRepository:
    # TODO: Find correct type for session
    def __init__(self, session: Any) -> None:
        self.session = session
