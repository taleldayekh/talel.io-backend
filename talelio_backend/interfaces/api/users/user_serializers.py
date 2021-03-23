from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    username = fields.Str()
    location = fields.Str()
    avatar_url = fields.Str()
