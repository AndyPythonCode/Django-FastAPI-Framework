from fastapi import status
from fastapi.responses import JSONResponse
from functools import wraps

"""
    functools es un módulo estándar de Python para funciones de orden superior 
    (funciones que actúan sobre otras funciones o las devuelven). wraps()
    es un decorador que se aplica a la función de envoltura de un decorador.
"""


def HTTP_404_NOT_FOUND(func):
    @wraps(func)
    async def wrapper(**kwrags):
            query = await func(**kwrags)
            if not query:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                    "message": "Item not found"
                })
            return query
    return wrapper

def HTTP_201_CREATED(func):
    @wraps(func)
    async def wrapper(*args, **kwrags):
            query = await func(*args, **kwrags)
            if type(query) is str:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                    "message": f"There a user with that {query}"
                })
            return query
    return wrapper
