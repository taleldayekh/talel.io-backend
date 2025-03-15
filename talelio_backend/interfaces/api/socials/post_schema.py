from marshmallow import Schema, fields, validate

from talelio_backend.interfaces.api.base_schema import CustomBaseSchema


class PostAudienceSchema(CustomBaseSchema):
    to = fields.List(fields.Str(), missing=[])
    cc = fields.List(fields.Str(), missing=[])


class PostMediaSchema(CustomBaseSchema):
    url = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(['image', 'video']))
    alt = fields.Str(required=True)


class PostSchema(CustomBaseSchema):
    content = fields.Str()
    media = fields.List(fields.Nested(PostMediaSchema), missing=[])
    audience = fields.Nested(PostAudienceSchema)


class CreatePostSchema(CustomBaseSchema):
    platforms = fields.List(fields.Str(),
                            required=True,
                            validate=validate.ContainsOnly(['mastodon', 'pixelfed', 'bluesky']))
    post = fields.Nested(PostSchema, required=True)
