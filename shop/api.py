import json
from random import randint
from datetime import date
from typing import Dict

from django.http import QueryDict
from django.db.models import Avg, Count, QuerySet
from django.core.paginator import Paginator
from django.conf import settings

from rest_framework import viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer

from .serializers import (
    TagSerializer,
    ProductCategorySerializer,
    ProductSerializer,
    ReviewProductSerializer,
    OrderSerializer,
    SaleSerializer,
)

from .models import (
    ProductCategory,
    Product,
    Tag,
    Basket,
    Order,
    OrderStatus,
    Sale,
)

from .services import (
    ProductFilter,
    sorting_products,
    get_list_products_in_basket,
    get_number_products_in_basket,
    adding_product_in_basket,
    delete_product_in_basket,
)


class ProductCategoryListApiView(ListAPIView):
    """
    ApiView для возврата категорий товаров
    """

    queryset: QuerySet = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('subcategories').prefetch_related('image')
    serializer_class: ModelSerializer = ProductCategorySerializer


class ProductDetailApiView(RetrieveAPIView):
    """
    ApiView для возврата детальная информация о товаре
    """

    queryset = Product.objects.all()
    serializer_class: ModelSerializer = ProductSerializer
    lookup_field: str = 'id'


class ProductReviewApiView(ListCreateAPIView):
    """
    ApiView для возврата и создания отзывов
    """

    serializer_class = ReviewProductSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=Product.objects.get(id=kwargs['id']))
        return self.list(request)


class CatalogListApiView(APIView):
    """
    ApiView для возврата каталога
    """

    def get(self, request: Request) -> Response:
        data_request: QueryDict = request.GET

        products: QuerySet = ProductFilter(
            {
                'price_min': request.GET.get('filter[minPrice]'),
                'price_max': request.GET.get('filter[maxPrice]'),
                'title': request.GET.get('filter[name]'),
                'freeDelivery': request.GET.get('filter[freeDelivery]'),
                'count': request.GET.get('filter[available]'),
                'category': request.GET.get('category'),
                'tags': request.GET.getlist('tags[]'),
            },
        ).qs

        products = sorting_products(
            queryset=products,
            sort=request.GET.get('sort'),
            sort_type=request.GET.get('sortType')
        )

        if products.exists():
            paginator = Paginator(products, settings.PAGINATE_BY)
            current_page: int = data_request.get('currentPage')
            last_page: int = paginator.num_pages

            serialized = ProductSerializer(
                paginator.get_page(current_page),
                many=True,
                fields=[
                    'id',
                    'category',
                    'price',
                    'count',
                    'date',
                    'title',
                    'description',
                    'freeDelivery',
                    'images',
                    'reviews'
                ],
                context={
                    'view': self
                }
            )

            return Response({'items': serialized.data,
                             'currentPage': current_page,
                             'lastPage': last_page})

        return Response({})


class ProductLimitedListApiView(APIView):
    """
    ApiView для возврата лимитированных товаров
    """

    def get(self, request: Request) -> Response:
        products: QuerySet = Product.objects.filter(limited_edition=True, count__gt=0)[:15]
        serialized = ProductSerializer(products,
                                       many=True,
                                       fields=[
                                           'id',
                                           'category',
                                           'price',
                                           'count',
                                           'date',
                                           'title',
                                           'description',
                                           'freeDelivery',
                                           'images',
                                           'tags',
                                           'reviews'
                                       ],
                                       context={'view': self})

        return Response(serialized.data)


class ProductPopularListApiView(APIView):
    """
    ApiView для возврата популярных товаров
    """

    def get(self, request: Request) -> Response:
        products: QuerySet = (
            Product.objects.filter(reviews__isnull=False)
            .annotate(reviews_count=Count('reviews'))
            .order_by('-reviews_count'))

        product_data = ProductSerializer(
            products,
            many=True,
            fields=[
                'id',
                'category',
                'price',
                'count',
                'date',
                'title',
                'description',
                'freeDelivery',
                'images',
                'tags',
                'reviews',

            ]
        ).data

        return Response(product_data)


class SalesListApiView(APIView):
    """
    ApiView для возврата скидок
    """

    def get(self, request: Request) -> Response:
        sales: QuerySet = Sale.objects.filter(date_to__gte=date.today()).order_by('date_to')

        if sales.exists():
            paginator = Paginator(sales, settings.PAGINATE_BY)
            current_page: int = request.GET.get('currentPage')
            last_page: int = paginator.num_pages

            items = SaleSerializer(
                paginator.get_page(current_page),
                many=True
            ).data

            data = {
                "items": items,
                "currentPage": current_page,
                "lastPage": last_page
            }
            return Response(data)

        return Response({})


class BannersListApiView(APIView):
    """
    ApiView для возврата баннера
    """

    def get(self, request: Request) -> Response:
        id_products_list: list = Product.objects.values_list('id', flat=True)
        banner_products: list = []

        for _ in range(3):
            id_product: list = id_products_list[randint(0, len(id_products_list) - 1)]
            product = Product.objects.get(id=id_product)

            product_data = ProductSerializer(
                product,
                fields=[
                    'id',
                    'category',
                    'price',
                    'count',
                    'date',
                    'title',
                    'description',
                    'freeDelivery',
                    'images',
                    'tags',
                    'reviews',

                ]
            ).data

            banner_products.append(product_data)
        return Response(banner_products)


class BasketListApiView(APIView):
    """
    ApiView для возврата, добавления, удаления товаров из корзину
    """

    def get(self, request: Request) -> Response:
        basket, products_in_basket = get_list_products_in_basket(request)
        count_products: Dict = get_number_products_in_basket(basket)

        serialized = ProductSerializer(products_in_basket,
                                       many=True,
                                       fields=['id',
                                               'category',
                                               'price',
                                               'count',
                                               'date',
                                               'title',
                                               'description',
                                               'freeDelivery',
                                               'images',
                                               'tags',
                                               'reviews'],
                                       context={
                                           'view': self,
                                           'count': count_products
                                       })

        return Response(serialized.data)

    def post(self, request: Request) -> Response:
        basket, products_in_basket = adding_product_in_basket(request)
        count_products: Dict = get_number_products_in_basket(basket)

        serialized = ProductSerializer(products_in_basket,
                                       many=True,
                                       fields=['id',
                                               'category',
                                               'price',
                                               'count',
                                               'date',
                                               'title',
                                               'description',
                                               'freeDelivery',
                                               'images',
                                               'tags',
                                               'reviews'],
                                       context={
                                           'view': self,
                                           'count': count_products
                                       })

        request.session['basket'] = basket.pk

        return Response(serialized.data)

    def delete(self, request: Request) -> Response:
        basket, products_in_basket = delete_product_in_basket(request)
        count_products: Dict = get_number_products_in_basket(basket)

        serialized = ProductSerializer(products_in_basket,
                                       many=True,
                                       fields=['id',
                                               'category',
                                               'price',
                                               'count',
                                               'date',
                                               'title',
                                               'description',
                                               'freeDelivery',
                                               'images',
                                               'tags',
                                               'reviews'],
                                       context={
                                           'view': self,
                                           'count': count_products
                                       })

        request.session['basket'] = basket.pk

        return Response(serialized.data)


class OrderListApiView(ListCreateAPIView):
    """
    ApiView для возврата списка заказов
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def post(self, request: Request, *args, **kwargs) -> Response:
        serialized = self.get_serializer(
            data={
                'totalCost': sum([product['price'] * product['count'] for product in request.data]),
            }
        )

        serialized.is_valid(raise_exception=True)
        serialized.save(status=OrderStatus.objects.get(status='На оформлении'))
        return Response({"orderId": serialized.instance.id})


class OrderDetailApiView(RetrieveUpdateAPIView):
    """
    ApiView для возврата и редактирования заказов
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'
    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request: Request, id: int) -> Response:
        serialized_order = self.get_serializer(Order.objects.get(id=id))
        response_data = dict()
        response_data.update(serialized_order.data)
        response_data['fullName'] = str(request.user.userprofile)
        response_data['phone'] = request.user.userprofile.phone
        response_data['email'] = request.user.email
        return Response(response_data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        serialised_order = self.get_serializer(self.get_object(),
                                               data=request.data)
        serialised_order.is_valid(raise_exception=True)
        serialised_order.save()
        basket_in_request: dict = request.data.get('basket')
        products = Product.objects.in_bulk(map(int, basket_in_request)).values()

        for product in products:
            product.count -= basket_in_request.get(str(product.id)).get('count')

        Product.objects.bulk_update(products, ['count'])
        basket_obj = Basket.objects.get(user=request.user)
        basket_obj.productsinbaskets_set.all().delete()
        basket_obj.delete()
        return Response(status=200)


class PaymentApiView(APIView):
    """
    ApiView для оплаты
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        order = Order.objects.get(id=kwargs['id'])
        order.status = OrderStatus.objects.get(status='Оплачен')
        order.save()
        return Response(status=200)


class TagViewSet(viewsets.ModelViewSet):
    """
    ApiView для отображения тегов
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
