from typing import Any

from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.data.repository import BaseRepository


class AccountRepository(BaseRepository):

    def create(self, account: Account, user: User) -> int:
        query = """
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
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (account.email, account.password, user.username,
                                       user.location, user.avatar_url))

                return cursor.fetchone()[0]

    def get_by_id(self, account_id: int) -> tuple[Any, ...]:
        query = """
            SELECT account.id,
                   account.created_at,
                   account.updated_at,
                   account.email,
                   account.password,
                   account.verified,
                   "user".id,
                   "user".username,
                   "user".location,
                   "user".avatar_url
            FROM account JOIN "user"
            ON account.id = "user".account_id
            WHERE account.id = %s;
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (account_id, ))

                return cursor.fetchone()

    def get_by_email(self, email: str) -> tuple[Any, ...]:
        query = """
            SELECT account.id,
                   account.created_at,
                   account.updated_at,
                   account.email,
                   account.password,
                   account.verified,
                   "user".id,
                   "user".username,
                   "user".location,
                   "user".avatar_url
            FROM account JOIN "user"
            ON account.id = "user".account_id
            WHERE account.email = %s;
            """

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (email, ))

                return cursor.fetchone()
