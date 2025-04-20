from marshmallow import Schema, fields


class WebFingerLinkSchema(Schema):
    rel = fields.Str(required=True)
    type = fields.Str(required=True)
    href = fields.Url(required=True)


class WebFingerSchema(Schema):
    subject = fields.Str(required=True)
    links = fields.List(fields.Nested(WebFingerLinkSchema), required=True)
