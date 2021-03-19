from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    location = fields.Str()
    avatar_url = fields.Str()
