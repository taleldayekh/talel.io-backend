from marshmallow import Schema, fields


class AccountSchema(Schema):
    email = fields.Str()
    password = fields.Str()
