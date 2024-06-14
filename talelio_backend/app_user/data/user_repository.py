from typing import Any

from talelio_backend.data.repository import BaseRepository


class UserRepository(BaseRepository):

    def get_by_id(self, user_id: int) -> tuple[Any, ...]:
        query = """
            SELECT * FROM "user" WHERE id = %s;
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (user_id, ))

                return cursor.fetchone()

    def get_by_username(self, username: str) -> tuple[Any, ...]:
        query = """
            SELECT * FROM "user" WHERE username = %s;
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (username, ))

                return cursor.fetchone()
