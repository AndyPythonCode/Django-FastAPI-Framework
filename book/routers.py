from fastapi import APIRouter
from .models import ModelBook

router_book = APIRouter(prefix='/book', tags=['Book'])

@router_book.get('')
def ListBook():
    item = [{'id':item.id, 'title':item.title, 'price':item.price} for item in ModelBook.objects.all()]
    return item