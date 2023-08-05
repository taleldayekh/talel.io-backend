from marshmallow import Schema, fields

from talelio_backend.interfaces.api.articles.article_schema import ArticleMetaSchema, ArticleSchema
from talelio_backend.interfaces.api.users.user_schema import UserSchema


class SerializeArticle(Schema):
    article = fields.Nested(ArticleSchema)
    user = fields.Nested(UserSchema(only=['id', 'username', 'location', 'avatar_url']))


class SerializeArticles(Schema):
    articles = fields.Nested(ArticleSchema, many=True)
    user = fields.Nested(UserSchema(only=['id', 'username', 'location', 'avatar_url']))

    # ! Should be optional for retrieving single article
    # meta = fields.Nested(ArticleMetaSchema)