from base64 import urlsafe_b64encode

from talelio_backend.data.uow import UnitOfWork
from talelio_backend.identity_and_access.webauthn_server import \
    generate_webauthn_registration_options
from talelio_backend.shared.exceptions import UserError


def get_passkey_registration_options(uow: UnitOfWork, user_id: int):
    with uow:
        user_record = uow.user.get_by_id(user_id)

        if not user_record:
            raise UserError('User not found')

        username = user_record['username']

        webauthn_credential_record = uow.webauthn.get_credentials_by_user_id(user_id)
        existing_credential_ids = [
            credential['credential_id'] for credential in webauthn_credential_record
        ]

        registration_options, registration_state = generate_webauthn_registration_options(
            user_id, username, existing_credential_ids)

        # ! Save state in redis
        # ! Map registration options to dataclass
        print('WebAuthn Registration Options:')
        print(registration_options)
        print(registration_state)
