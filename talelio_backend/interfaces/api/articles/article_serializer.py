from marshmallow import Schema, fields


class ArticleSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    title = fields.Str()
    slug = fields.Str()
    body = fields.Str()
    meta_description = fields.Str()
    html = fields.Str()
    featured_image = fields.Str()
    url = fields.Str()
