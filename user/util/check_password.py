from django.contrib.auth.hashers import check_password

def get_password_hash(password: str, passwordInDB: str):
    return check_password(password, passwordInDB)