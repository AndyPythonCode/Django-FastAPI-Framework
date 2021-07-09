from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

def unhash_django(password: str, passwordInDB: str):
    return check_password(password, passwordInDB)

def hash_django(password: str):
    return make_password(password)