from fastapi import Depends
from fastapi_users.db import BeanieUserDatabase

from app.models.user import User
from app.auth.auth import CustomFastAPIUsers
from app.auth.manager import UserManager
from app.auth.backend import jwt_authentication_backend, cookie_authentication_backend


async def get_user_db():
    yield BeanieUserDatabase(User)


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = CustomFastAPIUsers[User, int](
    get_user_manager, [jwt_authentication_backend, cookie_authentication_backend]
)

current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
