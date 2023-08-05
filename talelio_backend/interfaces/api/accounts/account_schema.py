from marshmallow import Schema, fields


class AccountSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    verified = fields.Bool()
    email = fields.Str()
