from dataclasses import dataclass
from os import getenv

from fido2.server import Fido2Server
from fido2.webauthn import (PublicKeyCredentialRpEntity, PublicKeyCredentialUserEntity,
                            UserVerificationRequirement)

RELYING_PARTY_ID = getenv('RELYING_PARTY_ID')
RELYING_PARTY_NAME = getenv('RELYING_PARTY_NAME')

if not RELYING_PARTY_ID or not RELYING_PARTY_NAME:
    raise ValueError(
        'Missing required environment variables: RELYING_PARTY_ID or RELYING_PARTY_NAME')


@dataclass(frozen=True)
class WebAuthnUser:
    id: int
    name: str

    def to_public_key_credential_user_entity(self) -> PublicKeyCredentialUserEntity:
        return PublicKeyCredentialUserEntity(
            id=str(self.id).encode('utf-8'),
            name=self.name,
            display_name=self.name,
        )


rp_entity = PublicKeyCredentialRpEntity(
    id=RELYING_PARTY_ID,
    name=RELYING_PARTY_NAME,
)

webauthn_server = Fido2Server(rp_entity)


def generate_webauthn_registration_options(user_id: int, username: str,
                                           existing_credential_ids: list[bytes]):
    user = WebAuthnUser(id=user_id, name=username).to_public_key_credential_user_entity()
    exclude_credentials = [{'id': id, 'type': 'public-key'} for id in existing_credential_ids]

    registration_options, registration_state = webauthn_server.register_begin(
        user=user,
        user_verification=UserVerificationRequirement.PREFERRED,
        exclude_credentials=exclude_credentials,
    )

    return registration_options, registration_state
