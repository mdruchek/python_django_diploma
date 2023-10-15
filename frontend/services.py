from django.db.models import QuerySet

from .models import (
    Product,
    ProductCategory
)


def filtering_products_by_price(products: QuerySet, min_price: int, max_price: int) -> QuerySet:
    """
    Фильтрация по цене

    :param products: Набор товаров
    :type products: QuerySet
    :param min_price: Минимальная цена
    :type min_price: int
    :param max_price: Максимальная цена
    :type max_price: int
    :return products: Отсортированные продукты
    :rtype products: QuerySet
    """

    products = products.filter(price__gte=min_price, price__lte=max_price)
    return products


def filtering_products_by_name(products, name) -> QuerySet:
    """
    Фильтрация по цене

    :param products: Набор товаров
    :type products: QuerySet
    :param name: Название товара
    :type name: str
    :return products: Отсортированные продукты
    :rtype products: QuerySet
    """

    products = products.filter(title__contains=name)
    return products


def filtering_product_by_category(products: QuerySet, category: int) -> QuerySet:
    """
    Фильтрация по категории

    :param products: Набор товаров
    :type products: QuerySet
    :param category: Категория товара
    :type category: int
    :return products: Отсортированные продукты
    :rtype products: QuerySet
    """

    category = ProductCategory.objects.get(id=category)
    if category.parent:
        products = products.filter(category=category)
    else:
        categories = ProductCategory.objects.filter(parent=category)
        products = products.filter(category__in=(category.id for category in categories))
    return products


def filtering_product_by_equality_key(products: QuerySet, **kwargs):
    """
    Фильтрация по флагу

    :param products: набор товаров
    :type products: QuerySet
    :param category: категория товара
    :type category: int
    :return products: Отсортированные продукты
    :rtype products: QuerySet
    """

    if list(kwargs.values())[0] == 'true':
        kwargs[list(kwargs.keys())[0]] = True
        products = products.filter(**kwargs)

    return products


class AddingProductInCartService:
    def adding_product(self):
        pass

    def delete_product(self):
        pass

    def change_number_products(self):
        pass

    def get_list_products(self):
        pass

    def get_number_products(self):
        pass


class AddingReviewProductService:
    def adding_review(self):
        pass

    def get_list_reviews(self):
        pass

    def get_discount_on_cart(self):
        pass

    def get_number_reviews(self):
        pass


class IntegrationWithPaymentService:
    def pay_order(self):
        pass

    def get_payment_status(self):
        pass
