from marshmallow import Schema, fields


class ArticleSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    title = fields.Str()
    body = fields.Str()
    html = fields.Str()
