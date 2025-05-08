from datetime import datetime
from typing import Any, TypedDict

from talelio_backend.data.repository import BaseRepository


class UserRecord(TypedDict):
    id: int
    account_id: int
    created_at: datetime
    updated_at: datetime
    username: str
    location: str
    avatar_url: str


class UserRepository(BaseRepository):

    def get_by_id(self, user_id: int) -> UserRecord | None:
        query = """
            SELECT * FROM "user" WHERE id = %s;
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (user_id, ))
                user_row = cursor.fetchone()

                if not user_row:
                    return None

                record = {
                    'id': user_row[0],
                    'account_id': user_row[1],
                    'created_at': user_row[2],
                    'updated_at': user_row[3],
                    'username': user_row[4],
                    'location': user_row[5],
                    'avatar_url': user_row[6],
                }

                return record

    def get_by_username(self, username: str) -> tuple[Any, ...]:
        query = """
            SELECT * FROM "user" WHERE username = %s;
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (username, ))

                return cursor.fetchone()
