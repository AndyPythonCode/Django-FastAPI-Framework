# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
from datetime import datetime, timedelta
from typing import Optional

from django.conf import settings
from user import schemas
from user.util.check_password import unhash_django
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt #python-jose [cryptography] to generate and verify JWT tokens in Python
from user.util import handler_error
from user.functions import query

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# check if match password hashed 
def verify_password(text_password: str, hashed_password: str):
    return unhash_django(text_password, hashed_password)


# Auth
async def authenticate_user(email: str, password: str):
    user = await query.get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# JWT
def create_access_token(data: dict, expired_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    # if i send to expired_delta check and calculate time
    if expired_delta:
        expire = datetime.utcnow() + expired_delta
    # otherwise add 15 by default
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # exp = Identifies the timestamp after which the JWT does not have to be accepted.
    to_encode.update({"exp": expire})
    # Encode the JWT and create a signature and expiration time
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Login token bearer
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # decode JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        # get signature
        email: str = payload.get('sub')
        if email is None:
            raise handler_error.CREDENTIALS_EXCEPTION
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise handler_error.CREDENTIALS_EXCEPTION
    user = await query.get_user(email=token_data.email)
    if user is None:
        raise handler_error.CREDENTIALS_EXCEPTION
    return user

# Create token
async def get_access_token(email: str, password: str):
    user = await authenticate_user(email, password)
    if not user:
        raise handler_error.EMAIL_AND_PASSWORD_EXCEPTION
    # A timedelta object represents a duration
    access_token_expires = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    # sub = Identifies the object or user who owns the JWT
    access_token = create_access_token(
        data={"sub": user.email}, expired_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}