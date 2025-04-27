from datetime import datetime
from typing import TypedDict

from talelio_backend.data.repository import BaseRepository


class WebAuthnRecord(TypedDict):
    credential_id: bytes
    created_at: datetime
    last_used_at: datetime | None
    device_name: str
    public_key: bytes
    sign_count: int


class WebAuthnRepository(BaseRepository):

    def get_credentials_by_user_id(self, user_id: int):
        query = """
                SELECT credential_id, created_at, last_used_at, device_name, public_key, sign_count
                FROM webauthn_credential
                WHERE user_id = %s;
            """
