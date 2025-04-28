from datetime import datetime
from typing import TypedDict, List

from talelio_backend.data.repository import BaseRepository


class WebAuthnRecord(TypedDict):
    credential_id: bytes
    created_at: datetime
    last_used_at: datetime | None
    device_name: str
    public_key: bytes
    sign_count: int


class WebAuthnRepository(BaseRepository):

    def get_credentials_by_user_id(self, user_id: int) -> List[WebAuthnRecord]:
        query = """
                SELECT credential_id, created_at, last_used_at, device_name, public_key, sign_count
                FROM webauthn_credential
                WHERE user_id = %s;
            """
        
        with self.session as session:
            with session.cursor() as cursor:
                cursor.execute(query, (user_id, ))
                webauthn_credential_rows = cursor.fetchall()

                record = [
                    {
                        'credential_id': row[0],
                        'created_at': row[1],
                        'last_used_at': row[2],
                        'device_name': row[3],
                        'public_key': row[4],
                        'sign_count': row[5],
                    }
                    for row in webauthn_credential_rows
                ]

                return record
