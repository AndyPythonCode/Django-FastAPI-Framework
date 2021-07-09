from typing import List, Dict
from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr
from user.functions import auth
from user.functions import query
from user.functions import permissions
from . import schemas


router_user = APIRouter(prefix='/auth', tags=['AUTH'])


# form OAuth2PasswordRequestFormCustom and depend on itself
# ACCESS_TOKEN_EXPIRE_HOURS = 12 in project/settings.py
@router_user.post('/token', response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.OAuth2PasswordRequestFormCustom = Depends()):
    """
    **Login access token.**
    
    **These are fields required:**

    {
        "username": "user@example.com",
        "password": "string"
    }

    """
    return await auth.get_access_token(form_data.username, form_data.password)


# REGISTER
@router_user.post('/register',
    response_model= Dict[str, str],
    summary= "Register user"
)
async def RegisterUser(request: schemas.User):
    """
    **Register user information.**

    **These are fields required:**

    {
        "email": "user@example.com",
        "password": "string"
    }

    
    """
    return await query.set_new_user(request)


# LIST
@router_user.get('/users', 
    response_model= List[schemas.UserOutSave],
    summary= "List user"
)
async def ListUser(current_user: schemas.User = Depends(permissions.get_current_staff_user)):
    """
    **Show user information.**

    Only staff and admin
    """
    return await query.get_all_users()


# UPDATE
@router_user.put('/update/{id}',
    response_model= Dict[str, str],
    summary= "Update user"
)
async def RegisterUser(id: int, request: schemas.UserUpdate, current_user: schemas.User = Depends(permissions.get_current_staff_user)):
    """
    **Update user information.**

    Only staff and admin

    **These are fields (Optional):**

    {
        "email": "user@example.com",
        "password": "******",
        "username": "string",
        "first_name": "string",
        "last_name": "string"
    }

    
    """
    return await query.update_user(id, request)


# DELETE
@router_user.delete('/delete',
    response_model= Dict[str, str],
    summary= "Delete user"
)
async def DeleteUser(request: EmailStr, current_user: schemas.User = Depends(permissions.get_current_admin_user)):
    """
    **Remove a user.**

    Only admin
    """
    return await query.delete_user(request)


# CURRENT USER
@router_user.get("/me", response_model=schemas.UserOutSave)
async def read_users_me(current_user: schemas.User = Depends(permissions.get_current_active_user)):
    """
    **Show current user information.**

    Only authentication
    """
    return current_user