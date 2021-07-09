from fastapi import Depends
from user import schemas
from user.util import handler_error
from user.functions.auth import get_current_user

async def get_current_active_user(current_user: schemas.UserOutSave = Depends(get_current_user)):
    if not current_user.is_active:
        raise handler_error.USER_INACTIVE
    return current_user

async def get_current_admin_user(current_user: schemas.UserOutSave = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise handler_error.USER_PERMISSION
    return current_user

async def get_current_staff_user(current_user: schemas.UserOutSave = Depends(get_current_user)):
    if not current_user.is_staff and not current_user.is_superuser:
        raise handler_error.USER_PERMISSION
    return current_user