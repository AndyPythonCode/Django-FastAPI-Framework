from asgiref.sync import sync_to_async
from user.util.handler_error import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from user.models import MyUser
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
    

    

