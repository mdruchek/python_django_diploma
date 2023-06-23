from django.db import models
from django.contrib.auth.models import User


class ProductSubcategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='Категория товара')
    is_active = models.BooleanField(default='True', verbose_name='Активна')


class ProductCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='Категория товара')
    is_active = models.BooleanField(default='True', verbose_name='Активна')
    subcategories = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE, verbose_name='Подкатегория')

    def __str__(self):
        return self.title


class UserRole(models.Model):
    title = models.CharField(max_length=100, verbose_name='Роль пользователя')

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    avatar = models.ImageField(verbose_name='Аватарка')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, verbose_name='Роль пользователя')


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Tag')


class Product(models.Model):
    price = models.FloatField(verbose_name='Стоимость')
    count = models.IntegerField(verbose_name='Количество')
    date = models.DateTimeField()
    title = models.CharField(max_length=100, verbose_name='Наименование')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    tags = models.ManyToManyField(Tag, verbose_name='Tags')
