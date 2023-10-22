from typing import Tuple, Dict

from django.db.models import QuerySet, Avg, Count

import django_filters

from rest_framework.request import Request

from .models import (
    Product,
    ProductCategory,
    Tag,
    Basket,
    ProductsInBaskets
)


def sorting_products(queryset: QuerySet, sort: str, sort_type: str) -> QuerySet:
    """
    Сортирует QuerySet товара

    :param queryset: queryset товара
    :type queryset: QuerySet
    :param sort: Параметр сортировки
    :type sort: str
    :param sort_type: Тип сортировки
    :type sort_type: str
    :return products: отсортированный queryset
    :rtype products: QuerySet
    """

    if sort_type == 'inc':
        sort_type = '-'
    else:
        sort_type = ''

    if sort == 'rating':

        products = queryset \
            .annotate(rating_avg=Avg('reviews__rate')) \
            .order_by('{sort_type}rating_avg'.format(sort_type=sort_type))

    elif sort == 'reviews':

        products = queryset \
            .annotate(reviews_count=Count('reviews')) \
            .order_by('{sort_type}reviews_count'.format(sort_type=sort_type))

    else:

        products = queryset \
            .order_by('{sort_type}{sort}'.format(sort_type=sort_type,
                                                 sort=sort))

    return products


class ProductFilter(django_filters.FilterSet):
    """
    Класс фильтрации товара
    """

    price = django_filters.RangeFilter()
    title = django_filters.CharFilter(lookup_expr='contains')
    freeDelivery = django_filters.BooleanFilter(method='filter_free_delivery')
    count = django_filters.BooleanFilter(method='filter_available')
    category = django_filters.NumberFilter(method='filter_category')
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())

    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'freeDelivery',
            'count',
            'category',
            'tags',
        ]

    def filter_free_delivery(self, queryset: QuerySet, name: str, value: bool) -> QuerySet:
        """
        Фильтрация по бесплатной доставке

        :param queryset: queryset товара
        :type queryset: QuerySet
        :param name: имя поля
        :type name: str
        :param value: значение для сортировки
        :type value: bool
        :return queryset: queryset товара
        :rtype queryset: QuerySet
        """

        if value:
            return queryset.filter(**{name: value})
        return queryset

    def filter_available(self, queryset: QuerySet, name: str, value: bool) -> QuerySet:
        """
        Фильтрация товара в наличии

        :param queryset: queryset товара
        :type queryset: QuerySet
        :param name: имя поля
        :type name: str
        :param value: значение для сортировки
        :type value: bool
        :return queryset: queryset товара
        :rtype queryset: QuerySet
        """

        if value:
            return queryset.filter(count__gt=0)
        return queryset

    def filter_category(self, queryset: QuerySet, name: str, value: int):
        """
        Фильтрация товара по категории

        :param queryset: queryset товара
        :type queryset: QuerySet
        :param name: имя поля
        :type name: str
        :param value: значение для сортировки
        :type value: int
        :return queryset: queryset товара
        :rtype queryset: QuerySet
        """

        category = ProductCategory.objects.get(id=value)
        if category.parent:
            return queryset.filter(category=category)
        else:
            categories = ProductCategory.objects.filter(parent=category)
            return queryset.filter(category__in=(category.id for category in categories))


def get_list_products_in_basket(request: Request) -> Tuple[Basket, QuerySet]:
    """
    Возвращает список товаров в корзине
    :param request: запрос
    :type request: Request
    :return basket: корзина
    :rtype basket: Basket
    :return products_in_basket:
    :rtype products_in_basket: QuerySet
    """

    basket_id: Basket = request.session.get('basket', False)

    if basket_id and request.user.is_authenticated:
        basket_user, basket_created = Basket.objects.get_or_create(user=request.user)
        basket_session = Basket.objects.get(id=basket_id)

        if not basket_created:
            products_in_basket_session = basket_session.products.all()
            products_in_basket_user = basket_user.products.all()

            for product in products_in_basket_session:

                if product not in products_in_basket_user:
                    basket_user.products.add(product,
                                             through_defaults={
                                                 'count': product.productsinbaskets_set.get(basket=basket_session,
                                                                                            product=product).count
                                             }
                                             )
            basket = basket_user

        else:
            basket_session.user = request.user
            basket_session.save()
            basket = basket_session

    elif basket_id and not request.user.is_authenticated:
        basket = Basket.objects.get(id=basket_id)

    elif not basket_id and request.user.is_authenticated:
        basket, basket_created = Basket.objects.get_or_create(user=request.user)

    elif not basket_id and not request.user.is_authenticated:
        return Product.objects.none()

    products_in_basket = basket.products.all()

    return basket, products_in_basket


def get_number_products_in_basket(basket: Basket) -> Dict[int, int]:
    """
    Возвращает количество товара в корзине
    :param basket: корзина
    :type basket: Basket
    :return count_products: словарь id товара и количества
    :rtype count_products: Dict
    """

    count_products = dict()
    for product_in_basket in (ProductsInBaskets.objects.filter(basket=basket).values()):
        count_products[product_in_basket['product_id']] = product_in_basket['count']
    return count_products


def combine_two_buckets(basket_user: Basket, basket_session: Basket) -> Basket:
    """
    Объединяет карзину неавторизованного пользователя с карзиной пользователя после авторизации

    :param basket_user: корзина авторизованного пользователя
    :type basket_user: Basket
    :param basket_session: корзина неавторизованного пользователя
    :type basket_session: Basket
    :return basket_user: объединённая карзина авторизованного пользователя
    :rtype basket_user: Basket
    """

    products_in_basket_session = basket_session.products.all()
    products_in_basket_user = basket_user.products.all()

    for product in products_in_basket_session:

        if product not in products_in_basket_user:
            basket_user.products.add(
                product,
                through_defaults={
                    'count': product.productsinbaskets_set.get(
                                basket=basket_session,
                                product=product
                            ).count
                }
            )

    return basket_user


class BasketService:

    def adding_product(self):
        pass

    def delete_product(self):
        pass

    def change_number_products(self):
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
