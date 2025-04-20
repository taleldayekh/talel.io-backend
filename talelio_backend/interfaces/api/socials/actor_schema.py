from marshmallow import Schema, fields


class ActorPublicKeySchema(Schema):
    id = fields.Url(required=True)
    owner = fields.Url(required=True)
    publicKeyPem = fields.Str(required=True)


class ActorSchema(Schema):
    context = fields.Url(data_key='@context', required=True)
    id = fields.Url(required=True)
    type = fields.Str(required=True)
    preferredUsername = fields.Str(required=True)
    followers = fields.Url(required=True)
    following = fields.Url(required=True)
    publicKey = fields.Nested(ActorPublicKeySchema, required=True)
