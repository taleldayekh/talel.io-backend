from marshmallow import Schema, fields

from talelio_backend.interfaces.api.users.user_serializers import UserSchema


class AccountSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    verified = fields.Bool()
    email = fields.Str()
    user = fields.Nested(UserSchema)
