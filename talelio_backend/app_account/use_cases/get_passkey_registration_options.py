from talelio_backend.data.uow import UnitOfWork
from talelio_backend.shared.exceptions import UserError
from base64 import urlsafe_b64encode
from os import getenv


def get_passkey_registration_options(uow: UnitOfWork, user_id: int):
    RELYING_PARTY_ID = getenv('RELYING_PARTY_ID')
    RELYING_PARTY_NAME = getenv('RELYING_PARTY_NAME')

    if not RELYING_PARTY_ID or not RELYING_PARTY_NAME:
        raise ValueError(
            'Missing "RELYING_PARTY_ID" or "RELYING_PARTY_NAME" environment variables'
        )

    with uow:
        user_record = uow.user.get_by_id(user_id)

        if not user_record:
            # TODO: Raise UserError
            pass
        
        username = user_record['username']
        passkey_user = {
            'id': user_id,
            'name': username,
            'display_name': username,
        }

        webauthn_credential_record = uow.webauthn.get_credentials_by_user_id(user_id)
        exclude_credentials = [
            {
                'id': urlsafe_b64encode(credential['credential_id']).rstrip(b'=').decode('utf-8'),
                'type': 'public-key',
            }
            for credential in webauthn_credential_record
        ]





        print('Exclude credentials')
        print(exclude_credentials)










# For Article
# Shows that it is expecting bytes
# https://github.com/Yubico/python-fido2/blob/22b1a11da7e7db9431f6c8f5955f4ccb1c11cafa/fido2/webauthn.py#L476
