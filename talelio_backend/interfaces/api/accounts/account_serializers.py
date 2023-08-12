from marshmallow import Schema, fields

from talelio_backend.interfaces.api.accounts.account_schema import AccountSchema
from talelio_backend.interfaces.api.users.user_schema import UserSchema


class SerializeAccount(Schema):
    account = fields.Nested(AccountSchema)
    user = fields.Nested(UserSchema(only=['id', 'username', 'location', 'avatar_url']))
