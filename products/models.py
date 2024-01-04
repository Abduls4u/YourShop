from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    storeName = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(null=True,)

    def __str__(self) -> str:
        return (self.name)
