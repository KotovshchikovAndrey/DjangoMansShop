from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    photo = models.ImageField(verbose_name='Фото Пользователя',upload_to='photos',blank=True)
    balans = models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Баланс Пользователя',default=0)
