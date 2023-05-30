from django.db import models
from django.contrib.auth.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория товара')
    is_active = models.BooleanField(default='True', verbose_name='Активна')

    def __str__(self):
        return self.name


class UserRole(models.Model):
    name = models.CharField(max_length=100, verbose_name='Роль пользователя')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    avatar = models.ImageField(verbose_name='Аватарка')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, verbose_name='Роль пользователя')
