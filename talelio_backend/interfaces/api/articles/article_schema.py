from marshmallow import Schema, fields


class ArticleSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    title = fields.Str()
    slug = fields.Str()
    body = fields.Str()
    html = fields.Str()
    meta_description = fields.Str()
    table_of_contents = fields.Str()
    featured_image = fields.Str()
    url = fields.Str()


class NextAndPrevArticleSchema(Schema):
    title = fields.Str()
    slug = fields.Str()


class AdjacentArticlesSchema(Schema):
    next = fields.Nested(NextAndPrevArticleSchema)
    prev = fields.Nested(NextAndPrevArticleSchema)


class ArticleMetaSchema(Schema):
    adjacent_articles = fields.Nested(AdjacentArticlesSchema)
