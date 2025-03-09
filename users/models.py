
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    is_seller = models.BooleanField(default=False, verbose_name='Продавец')

    def str(self):
        return f"{self.email} - {self.is_seller}"


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer')
    address = models.TextField(blank=True, default='', verbose_name='Адрес')

    def str(self):
        return f"{self.user.name}{self.address}"


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    upd = models.CharField(max_length=50, default='', verbose_name='Уникальный номер покупателя', blank=True)
    legal_name = models.CharField(max_length=100, default='', verbose_name='Юридическое имя', blank=True)
    profile_pic = models.ImageField(blank=True, default='Add you photo...', verbose_name='Фото', upload_to='seller')
    facebook = models.CharField(max_length=50, default='', blank=True)
    vk = models.CharField(max_length=50, default='', blank=True)
    instagram = models.CharField(max_length=50, default='', blank=True)
    telegram = models.CharField(max_length=50, default='', blank=True)

    def str(self):
        return self.legal_name