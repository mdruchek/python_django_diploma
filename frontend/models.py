from django.db import models
from django.contrib.auth.models import User


class ImageDepartments(models.Model):
    src = models.CharField(max_length=500, verbose_name='Путь')
    alt = models.CharField(max_length=50, verbose_name='Описание')


class ProductCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='Категория товара')
    is_active = models.BooleanField(default='True', verbose_name='Активна')
    image = models.ForeignKey(ImageDepartments, on_delete=models.PROTECT, verbose_name='Иконка')

    def __str__(self):
        return self.title


class ProductSubcategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='Категория товара')
    is_active = models.BooleanField(default='True', verbose_name='Активна')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')

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
    category = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE, verbose_name='Подкатегория')
    price = models.FloatField(verbose_name='Стоимость')
    count = models.IntegerField(verbose_name='Количество')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.CharField(max_length=500, verbose_name='Описание')
    fullDescription = models.TextField(max_length=1000, verbose_name='Полное описание')
    freeDelivery = models.BooleanField(default=False, verbose_name='Бесплатная доставка')
    tags = models.ManyToManyField(Tag, verbose_name='Tags')


def image_product_directory_path(instance: 'ImagesProducts', filename: str) -> str:
    return 'img/products/product_{pk}/{filename}'.format(pk=instance.product.pk, filename=filename)


class ImagesProducts(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to=image_product_directory_path, verbose_name='Фото товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
