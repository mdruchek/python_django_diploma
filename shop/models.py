from django.db import models
from django.contrib.auth.models import User


class ImageDepartments(models.Model):
    src = models.CharField(verbose_name='путь', max_length=500, blank=True, null=True)
    alt = models.CharField(verbose_name='описание', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'изображение категории товара'
        verbose_name_plural = 'изображения категорий товара'
        db_table = 'frontend_imagedepartments'

    def __str__(self):
        return self.src


class ProductCategory(models.Model):
    title = models.CharField(verbose_name='категория товара', max_length=100)
    parent = models.ForeignKey('self',
                               models.DO_NOTHING,
                               db_column='parent',
                               related_name='subcategories',
                               verbose_name='родительская категория',
                               blank=True,
                               null=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)
    image = models.ForeignKey(ImageDepartments, verbose_name='иконка', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = 'категория продукта'
        verbose_name_plural = 'категории товаров'
        db_table = 'frontend_productcategory'

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(verbose_name='тэг', max_length=100)

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'
        db_table = 'frontend_tag'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, verbose_name='категория', on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='стоимость')
    count = models.IntegerField(verbose_name='количество')
    date = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    title = models.CharField(verbose_name='наименование', max_length=100, db_index=True)
    description = models.CharField(verbose_name='описание', max_length=500)
    fullDescription = models.TextField(max_length=1000, verbose_name='полное описание')
    freeDelivery = models.BooleanField(verbose_name='бесплатная доставка', default=False)
    tags = models.ManyToManyField(Tag, verbose_name='тэги', blank=True, null=True)
    limited_edition = models.BooleanField(verbose_name='ограниченный тираж', default=False)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товар'
        db_table = 'frontend_product'

    def __str__(self):
        return self.title


def image_product_directory_path(instance: 'ImagesProducts', filename: str) -> str:
    return 'img/products/product_{pk}/{filename}'.format(pk=instance.product.pk, filename=filename)


class ImagesProducts(models.Model):
    src = models.ImageField(verbose_name='фото товара', upload_to=image_product_directory_path)
    alt = models.CharField(verbose_name='описание', max_length=50, default='Image alt string')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'изображение товара'
        verbose_name_plural = 'изображения товара'
        db_table = 'frontend_imagesproducts'

    def __str__(self):
        return self.src.name


class Basket(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.PROTECT, blank=True, null=True)
    products = models.ManyToManyField(Product,
                                      verbose_name='товар',
                                      through='ProductsInBaskets',
                                      through_fields=('basket', 'product'))

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'
        db_table = 'frontend_basket'


class ProductsInBaskets(models.Model):
    basket = models.ForeignKey(Basket, verbose_name='корзина', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.PROTECT)
    count = models.IntegerField(verbose_name='количество')

    class Meta:
        db_table = 'frontend_productsinbaskets'


class OrderStatus(models.Model):
    status = models.CharField(verbose_name='статус', max_length=50)

    class Meta:
        verbose_name = 'статус заказа'
        verbose_name_plural = 'статаусы заказов'
        db_table = 'frontend_orderstatus'

    def __str__(self):
        return self.status


class Order(models.Model):
    createdAt = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    fullName = models.CharField(verbose_name='полное имя пользователя', max_length=100, null=True, blank=True)
    email = models.EmailField(verbose_name='email', max_length=100, null=True, blank=True)
    phone = models.CharField(verbose_name='номер телефона', max_length=12, null=True, blank=True)
    deliveryType = models.CharField(verbose_name='тип доставки', max_length=20, null=True, blank=True)
    paymentType = models.CharField(verbose_name='тип оплаты', max_length=20, null=True, blank=True)
    totalCost = models.FloatField(verbose_name='полная стоимость', null=True, blank=True)
    status = models.ForeignKey(OrderStatus, verbose_name='статус заказа', on_delete=models.PROTECT)
    city = models.CharField(verbose_name='город', max_length=50, null=True, blank=True)
    address = models.CharField(verbose_name='адрес', max_length=100, null=True, blank=True)
    products = models.ManyToManyField(Product,
                                      verbose_name='товар',
                                      through='ProductsInOrders',
                                      through_fields=('order', 'product'))

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        db_table = 'frontend_order'


class ProductsInOrders(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.PROTECT)
    count = models.IntegerField(verbose_name='количество')

    class Meta:
        db_table = 'frontend_productsinorders'


class ReviewProduct(models.Model):
    author = models.CharField(verbose_name='автор', max_length=50)
    email = models.EmailField(verbose_name='email', max_length=100)
    text = models.CharField(verbose_name='текст отзыва', max_length=500)
    rate = models.IntegerField(verbose_name='оценка')
    date = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = 'отзыв о товаре'
        verbose_name_plural = 'отзывы о товарах'
        db_table = 'frontend_reviewproduct'


class SpecificationProduct(models.Model):
    name = models.CharField(verbose_name='название', max_length=100)
    value = models.CharField(verbose_name='значение', max_length=100)
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.CASCADE, related_name='specifications')

    class Meta:
        verbose_name = 'характеристика товара'
        verbose_name_plural = 'характеристики товаров'
        db_table = 'frontend_specificationproduct'


class Sale(models.Model):
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.CASCADE)
    sale_price = models.FloatField(verbose_name='цена со скидкой')
    date_from = models.DateField(verbose_name='начало')
    date_to = models.DateField(verbose_name='конец')

    class Meta:
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'
        db_table = 'frontend_sale'
