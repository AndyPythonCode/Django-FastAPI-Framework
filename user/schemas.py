from fastapi.param_functions import Form, Query
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm

class User(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str] = Query(..., min_length=5)
    first_name: Optional[str] = Query(..., min_length=1)
    last_name: Optional[str] = Query(..., min_length=1)
    username: Optional[str] = Query(..., min_length=1)

class UserInput(User):
    id: int
    date_joined: datetime
    last_login: Optional[datetime]
    is_active: bool
    is_superuser: bool
    is_staff: Optional[bool]

class UserOutSave(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_superuser: bool
    is_staff: Optional[bool]
    date_joined: datetime
    last_login: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
            "id": 1,
            "email": "admin@gmail.com",
            "username": "admin",
            "first_name": "admin",
            "last_name": "admin",
            "is_active": True,
            "is_superuser": False,
            "is_staff": True,
            "last_login": "2021-07-04T20:01:46.901316+00:00",
            "date_joined": "2021-07-04T19:29:55.308208+00:00"
            },
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# overwriting default form-data fastapi
class OAuth2PasswordRequestFormCustom(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(None, regex="password"),
        username: EmailStr = Form(...),
        password: str = Form(...),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        super().__init__(grant_type, username, password, scope, client_id, client_secret)