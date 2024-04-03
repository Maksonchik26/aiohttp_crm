import uuid

from aiohttp.web_response import json_response

from app.crm.models import User
from app.web.app import View


class AddUserView(View):
    async def post(self):
        data = await self.request.json()
        user = User(id_=uuid.uuid4(), email=data["email"])
        await self.request.app.crm_accessor.add_user(user)
        return json_response(data={"status": "ok"})


class ListUsersView(View):
    async def get(self):
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [{"email": user.email, "id": str(user.id_)} for user in users]

        return json_response({"status": "ok", "users": raw_users})


class GetUserView(View):
    async def get(self):
        user_id = self.request.query["id"]
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        return json_response({"status": "ok", "user": {"email": user.email, "id": str(user.id_)}})
