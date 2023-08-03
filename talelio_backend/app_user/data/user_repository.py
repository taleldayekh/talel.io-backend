from talelio_backend.shared.data.repository import BaseRepository


class UserRepository(BaseRepository):

    def get_by_username(self, username: str):
        QUERY = (f"""
            SELECT * FROM "user" WHERE username = %s;
            """)

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(QUERY, (username, ))

                return cursor.fetchall()
