from django.db import models

# Create your models here.
class ModelBook(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)