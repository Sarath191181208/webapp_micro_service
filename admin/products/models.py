from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=2083)
    likes = models.IntegerField(default=0)

class User(models.Model):
    ... 
    # name = models.CharField(max_length=255)
    # email = models.CharField(max_length=255)
    # password = models.CharField(max_length=255)
