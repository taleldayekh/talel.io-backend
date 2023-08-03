from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.shared.data.repository import BaseRepository


class AccountRepository(BaseRepository):

    def create(self, account: Account, user: User) -> int:
        QUERY = (f"""
            WITH created_account AS
            (
                INSERT INTO account (email, password)
                VALUES (%s, %s)
                RETURNING id
            )
            INSERT INTO "user" (username, location, avatar_url, account_id)
            SELECT %s, %s, %s, id
            FROM created_account
            RETURNING account_id;
            """)

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(QUERY, (account.email, account.password, user.username,
                                       user.location, user.avatar_url))

                return cursor.fetchone()[0]

    def get_by_email(self, email: str):
        QUERY = (f"""
            SELECT * FROM account WHERE email = %s;
            """)

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(QUERY, (email, ))

                return cursor.fetchall()
