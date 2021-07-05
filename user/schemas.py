from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    date_joined: datetime
    last_login: datetime
    is_superuser: bool
    is_staff: bool
    is_active: bool

class UserInPut(User):
    password: str

class UserOutPut(User):
    id: int

    class Config:
        schema_extra = {
            "example": {
            "id": 1,
            "last_login": "2021-07-04T20:01:46.901316+00:00",
            "is_superuser": True,
            "first_name": "admin",
            "last_name": "admin",
            "is_staff": True,
            "is_active": True,
            "date_joined": "2021-07-04T19:29:55.308208+00:00",
            "email": "admin@gmail.com",
            "username": "admin"
            },
        }
