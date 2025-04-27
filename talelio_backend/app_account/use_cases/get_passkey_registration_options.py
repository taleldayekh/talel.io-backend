from talelio_backend.data.uow import UnitOfWork
from talelio_backend.shared.exceptions import UserError


def get_passkey_registration_options(uow: UnitOfWork, user_id: int):
    with uow:
        user_record = uow.user.get_by_id(user_id)

        if not user_record:
            # TODO: Raise UserError
            pass

        # TODO: Return user record, need to make a mapping.
        passkey_user = {'': ''}

        # Get exclude credentials...

        print(user_record)


# For Article
# Shows that it is expecting bytes
# https://github.com/Yubico/python-fido2/blob/22b1a11da7e7db9431f6c8f5955f4ccb1c11cafa/fido2/webauthn.py#L476
