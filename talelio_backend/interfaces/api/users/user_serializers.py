from marshmallow import Schema, fields

from talelio_backend.interfaces.api.articles.article_serializer import ArticleSchema


class UserSchema(Schema):
    id = fields.Int()
    account_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    username = fields.Str()
    location = fields.Str()
    avatar_url = fields.Str()


class UserArticlesSchema(Schema):
    user = fields.Nested(UserSchema(only=['username', 'location', 'avatar_url']))
    articles = fields.Nested(ArticleSchema(many=True, exclude=['user_id']))
