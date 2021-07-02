from django.contrib import admin
from .models import ModelBook

# Register your models here.
@admin.register(ModelBook)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','title','price')