from django.db.models import QuerySet, Avg, Count

import django_filters

from .models import (
    Product,
    ProductCategory,
    Tag,
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
