from asgiref.sync import sync_to_async
from user.util.handler_error import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from user.util.check_password import hash_django
from user.models import MyUser
from user import schemas
# This file for every query on database

@HTTP_404_NOT_FOUND
@sync_to_async
def get_all_users():
    query = MyUser.objects.all()

    output = [
        {
            "id": data.id,
            "last_login": data.last_login,
            "is_superuser": data.is_superuser,
            "first_name": data.first_name,
            "last_name": data.last_name,
            "is_staff": data.is_staff,
            "is_active": data.is_active,
            "date_joined": data.date_joined,
            "email": data.email,
            "username": data.username 
        }
    for data in query ]

    return output


@HTTP_404_NOT_FOUND
@sync_to_async
def delete_user(email):
    query = MyUser.objects.filter(email__exact=email)

    if not query:
        return False
    
    query.delete()
    return {'user':'removed'}


@HTTP_404_NOT_FOUND
@sync_to_async
def update_user(id, user: schemas.UserUpdate):
    query = MyUser.objects.filter(pk=id)

    if not query:
        return False
    
    #Hashing new password
    user.password = hash_django(user.password)
    query.update(**user.dict())
            
    return {'user':'updated'}


@HTTP_201_CREATED
@sync_to_async
def set_new_user(user):
    user = user.dict()

    # Validation if exists
    username = MyUser.objects.filter(username__exact=user['username'])
    email = MyUser.objects.filter(email__exact=user['email'])

    if email:
        return 'email'
    
    if username:
        return 'username'

    MyUser.objects.create_user(**user).save()
    return {'user':'added'}
    

# Look for a user
@sync_to_async
def get_user(email: str):
    user = MyUser.objects.filter(email=email).first()
    if user:
        # Return data with this schema
        return schemas.UserInput(**user.__dict__)

