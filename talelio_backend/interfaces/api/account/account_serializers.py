from marshmallow import Schema, fields

from talelio_backend.interfaces.api.user.user_serializers import UserSchema


class AccountSchema(Schema):
    id = fields.Int()
    verified = fields.Bool()
    email = fields.Str()
    user = fields.Nested(UserSchema)
