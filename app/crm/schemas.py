from marshmallow import Schema, fields

from app.web.schemas import OkResponseSchema


class CreateUserSchema(Schema):
    email = fields.Str(required=True)


class UserSchema(CreateUserSchema):
    id = fields.UUID(required=True, attribute="id_")


class GetUserRequestSchema(Schema):
    id = fields.UUID(required=True)


class GetUserResponseSchema(OkResponseSchema):
    data = fields.Nested(UserSchema)


class ListUserSchema(Schema):
    users = fields.Nested(UserSchema, many=True)


class ListUserResponseSchema(OkResponseSchema):
    data = fields.Nested(ListUserSchema)



