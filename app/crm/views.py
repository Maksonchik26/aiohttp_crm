import uuid


from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema

from app.crm.models import User
from app.crm.schemas import (UserSchema,
                             ListUserResponseSchema,
                             GetUserRequestSchema,
                             CreateUserSchema,
                             GetUserResponseSchema)
from app.web.app import View
from app.web.schemas import OkResponseSchema
from app.web.utils import json_response, check_basic_auth


class AddUserView(View):
    @docs(tags=["crm"], summary="Add new user", description="Add new user to DB")
    @request_schema(CreateUserSchema) # Исп-ся для тела запроса (json)
    @response_schema(OkResponseSchema(), 200)
    async def post(self):
        data = self.request["data"] # Без await т.к. данные уже получены и провалидированы и не нужно ходить в сокет
        user = User(id_=uuid.uuid4(), email=data["email"])
        await self.request.app.crm_accessor.add_user(user)

        return json_response()


class ListUsersView(View):
    @docs(tags=["crm"], summary="List users", description="List users from DB")
    @response_schema(ListUserResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get("Authorization"):
            raise HTTPUnauthorized
        if not check_basic_auth(self.request.headers.get("Authorization"),
                                self.request.app.config.username,
                                self.request.app.config.password):
            raise HTTPForbidden

        users = await self.request.app.crm_accessor.list_users()
        raw_users = [UserSchema().dump(user) for user in users]

        return json_response(data={"users": raw_users})


class GetUserView(View):
    @docs(tags=["crm"], summary="Get user", description="Get user from DB")
    @querystring_schema(GetUserRequestSchema)
    @response_schema(GetUserResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get("Authorization"):
            raise HTTPUnauthorized
        if not check_basic_auth(self.request.headers.get("Authorization"),
                                self.request.app.config.username,
                                self.request.app.config.password):
            raise HTTPForbidden
        user_id = self.request.query["id"]
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            return json_response(data={"user": UserSchema().dump(user)})
        raise HTTPNotFound
