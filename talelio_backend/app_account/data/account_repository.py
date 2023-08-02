from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.shared.data.repository import BaseRepository


class AccountRepository(BaseRepository):

    def create(self, account: Account, user: User):
        QUERY = (f"""
            WITH created_account AS
            (
                INSERT INTO account (email, password)
                VALUES (%s, %s)
                RETURNING id
            )
            """)

        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(QUERY, (account.email, account.password))
