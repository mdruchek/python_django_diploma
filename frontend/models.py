from django.db import models
from django.contrib.auth.models import User


class ImageDepartments(models.Model):
    src = models.CharField(max_length=500, verbose_name='Путь', blank=True, null=True)
    alt = models.CharField(max_length=50, verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Изображение категории товара'
        verbose_name_plural = 'Изображения категорий товара'

    def __str__(self):
        return self.src


class ProductCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='Категория товара')
    parent = models.ForeignKey('self',
                               models.DO_NOTHING,
                               db_column='parent',
                               related_name='subcategories',
                               verbose_name='Родительская категория',
                               blank=True,
                               null=True)
    is_active = models.BooleanField(default='True', verbose_name='Активна')
    image = models.ForeignKey(ImageDepartments, on_delete=models.PROTECT, verbose_name='Иконка', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.title


class UserRole(models.Model):
    title = models.CharField(max_length=100, verbose_name='Роль пользователя')

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'

    def __str__(self):
        return self.title


class UserAvatar(models.Model):
    src = models.ImageField(verbose_name='Аватар')
    alt = models.CharField(verbose_name='Описание', max_length=50, default='User avatar')
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Аватарка пользователя'
        verbose_name_plural = 'Аватарки пользователей'


class UserProfile(models.Model):
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', blank=True)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, verbose_name='Роль пользователя')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return '{last_name} {fist_name} {patronymic}'.format(patronymic=self.patronymic,
                                                             fist_name=self.user.first_name,
                                                             last_name=self.user.last_name)


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Tag')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.FloatField(verbose_name='Стоимость')
    count = models.IntegerField(verbose_name='Количество')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    title = models.CharField(max_length=100, verbose_name='Наименование', db_index=True)
    description = models.CharField(max_length=500, verbose_name='Описание')
    fullDescription = models.TextField(max_length=1000, verbose_name='Полное описание')
    freeDelivery = models.BooleanField(default=False, verbose_name='Бесплатная доставка')
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True, null=True)
    limited_edition = models.BooleanField(verbose_name='Ограниченный тираж', default=False)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товар'

    def __str__(self):
        return self.title


def image_product_directory_path(instance: 'ImagesProducts', filename: str) -> str:
    return 'img/products/product_{pk}/{filename}'.format(pk=instance.product.pk, filename=filename)


class ImagesProducts(models.Model):
    src = models.ImageField(upload_to=image_product_directory_path, verbose_name='Фото товара')
    alt = models.CharField(verbose_name='описание', max_length=50, default='Image alt string')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='images')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'

    def __str__(self):
        return self.src.name


class Basket(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT, blank=True, null=True)
    products = models.ManyToManyField(Product,
                                      verbose_name='Товар',
                                      through='ProductsInBaskets',
                                      through_fields=('basket', 'product'))


class ProductsInBaskets(models.Model):
    basket = models.ForeignKey(Basket, verbose_name='Корзина', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.PROTECT)
    count = models.IntegerField(verbose_name='Количество')


class OrderStatus(models.Model):
    status = models.CharField(verbose_name='Статус', max_length=50)

    def __str__(self):
        return self.status


class Order(models.Model):
    createdAt = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    fullName = models.CharField(verbose_name='Полное имя пользователя', max_length=100, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=100, null=True, blank=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=12, null=True, blank=True)
    deliveryType = models.CharField(verbose_name='Тип доставки', max_length=20, null=True, blank=True)
    paymentType = models.CharField(verbose_name='Тип оплаты', max_length=20, null=True, blank=True)
    totalCost = models.FloatField(verbose_name='Полная стоимость', null=True, blank=True)
    status = models.ForeignKey(OrderStatus, verbose_name='Статус заказа', on_delete=models.PROTECT)
    city = models.CharField(verbose_name='Город', max_length=50, null=True, blank=True)
    address = models.CharField(verbose_name='Адрес', max_length=100, null=True, blank=True)
    products = models.ManyToManyField(Product,
                                      verbose_name='Товар',
                                      through='ProductsInOrders',
                                      through_fields=('order', 'product'))


class ProductsInOrders(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.PROTECT)
    count = models.IntegerField(verbose_name='Количество')


class ReviewProduct(models.Model):
    author = models.CharField(verbose_name='Автор', max_length=50)
    email = models.EmailField(verbose_name='Email', max_length=100)
    text = models.CharField(verbose_name='Текст отзыва', max_length=500)
    rate = models.IntegerField(verbose_name='Оценка')
    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = 'Отзыв о товаре'
        verbose_name_plural = 'Отзывы о товарах'


class SpecificationProduct(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    value = models.CharField(verbose_name='Значение', max_length=100)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='specifications')

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'


class Sale(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    sale_price = models.FloatField(verbose_name='цена со скидкой')
    date_from = models.DateField(verbose_name='начало')
    date_to = models.DateField(verbose_name='конец')

    class Meta:
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'
