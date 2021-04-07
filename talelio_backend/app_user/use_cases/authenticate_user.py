from typing import Dict

from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.core.auth import check_password_hash, generate_access_token
from talelio_backend.core.exceptions import AccountError
from talelio_backend.data.uow import UnitOfWork


def get_access_token(uow: UnitOfWork, email: str, password: str) -> Dict[str, str]:
    error_msg = 'Invalid username or password'

    with uow:
        account_record = uow.account.get(Account, email=email)

        if account_record is None:
            raise AccountError(error_msg)

        password_hash = account_record.password

        if not check_password_hash(password, password_hash):
            raise AccountError(error_msg)

        payload = {'user_id': account_record.user.id, 'username': account_record.user.username}
        access_token = generate_access_token(payload)

        return {'access_token': access_token}
