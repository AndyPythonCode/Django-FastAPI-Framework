from typing import List, Dict
from fastapi import APIRouter
from .functions.query import get_all_users, set_new_user
from .util.check_password import get_password_hash
from .schemas import UserOutPut, UserInPut
from .models import MyUser

router_user = APIRouter(prefix='/user', tags=['USERS'])

@router_user.get('/', 
    response_model= List[UserOutPut],
    summary= "List user"
)
async def ListUser():
    """
    **Show user information.**
    """
    return await get_all_users()


@router_user.post('/create',
    response_model= Dict[str, str],
    summary= "Create user"
)
async def CreateUser(request: UserInPut):
    """
    **Create user information.**
    """
    return await set_new_user(request)


def Check(request: str):
    return get_password_hash(request, MyUser.objects.all().first().password)