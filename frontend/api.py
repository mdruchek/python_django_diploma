import json
from django.http import HttpRequest, HttpResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.admin import User
from django.db import IntegrityError, transaction
from django.db.models import Avg, QuerySet
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import (TagSerializer,
                          ProductCategorySerializer,
                          ProductSerializer,
                          ReviewProductSerializer,
                          OrderSerializer
                          )
from .models import (UserProfile,
                     UserAvatar,
                     UserRole,
                     ProductCategory,
                     Product,
                     ReviewProduct,
                     Tag,
                     Basket,
                     ProductsInBaskets,
                     Order,
                     ProductsInOrders,
                     OrderStatus)


class ProductCategoryListApiView(ListAPIView):
    queryset = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('subcategories').prefetch_related('image')
    serializer_class = ProductCategorySerializer


class ProductDetailApiView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'


class ProductReviewApiView(ListCreateAPIView):
    serializer_class = ReviewProductSerializer

    def create(self, request, *args, **kwargs):
        self.queryset = ReviewProduct.objects.filter(product_id=kwargs['id'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=Product.objects.get(id=kwargs['id']))
        return self.list(request)


class CatalogListApiView(APIView):
    def get(self, request):
        data_request: QueryDict = request.GET

        products = ((Product.objects.filter(price__gte=int(data_request.get('filter[minPrice]', 0)),
                                            price__lte=int(data_request.get('filter[maxPrice]', 500000)))
                     .prefetch_related('images'))
                    .prefetch_related('reviews'))

        if data_request.get('category', False):
            category = ProductCategory.objects.get(id=data_request['category'])
            if category.parent:
                products = products.filter(category=data_request['category'])
            else:
                categories = ProductCategory.objects.filter(parent=category)
                products = products.filter(category__in=(category.id for category in categories))

        if data_request.get('filter[name]', ''):
            products = products.filter(title__contains=data_request['filter[name]'])

        if data_request.get('filter[freeDelivery]', False) == 'true':
            products = products.filter(freeDelivery=True)

        if data_request.get('filter[available]') == 'true':
            products = products.filter(count__gt=0)

        if data_request.get('sortType') == 'inc':
            sort_type = '-'
        else:
            sort_type = ''

        sort = data_request.get(key='sort', default='title')

        if sort == 'rating':
            products = sorted(products,
                              key=(lambda obj: round(ReviewProduct.objects.filter(product=obj).aggregate(Avg('rate'))['rate__avg'], 1)
                              if ReviewProduct.objects.filter(product=obj) else 0),
                              reverse=True if sort_type =='-' else False)
        elif sort == 'reviews':
            products = sorted(products,
                              key=(lambda obj: obj.reviews.all().count()),
                              reverse=True if sort_type == '-' else False)
        else:
            products = products.order_by('{sort_type}{sort}'.format(sort_type=sort_type,
                                                                    sort=sort))

        tags = data_request.getlist('tags[]')
        if tags:
            products = Product.objects.filter(tags__in=tags)

        paginator = Paginator(products, 2)
        current_page = data_request.get('currentPage')
        last_page = paginator.num_pages

        serialized = ProductSerializer(paginator.get_page(current_page),
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
                                       context={'view': self})

        return Response({'items': serialized.data,
                         'currentPage': current_page,
                         'lastPage': last_page})


class ProductLimitedListApiView(APIView):
    def get(self, request):
        products = Product.objects.filter(limited_edition=True, count__gt=0)[:15]
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
    def get(self, request):
        # products = Product.objects.filter()
        data = [{
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
              {
                "src": "/3.png",
                "alt": "Image alt string"
              }
            ],
            "tags": [
              {
                "id": 12,
                "name": "Gaming"
              }
            ],
            "reviews": 5,
            "rating": 4.6
        }]
        return Response(data)


class SalesListApiView(APIView):
    def get(self, request):
        data = {
          "items": [
            {
              "id": "123",
              "price": 500.67,
              "salePrice": 200.67,
              "dateFrom": "2023-05-08",
              "dateTo": "2023-05-20",
              "title": "video card",
              "images": [
                "string"
              ]
            }
          ],
          "currentPage": 5,
          "lastPage": 10
        }
        return Response(data)


class BannersListApiView(APIView):
    def get(self, request):
        data = [
          {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
              {
                "src": "/3.png",
                "alt": "Image alt string"
              }
            ],
            "tags": [
              {
                "id": 12,
                "name": "Gaming"
              }
            ],
            "reviews": 5,
            "rating": 4.6
          }
        ]
        return Response(data)


class BasketListApiView(APIView):
    def get(self, request: Request):
        basket_id: Basket = request.session.get('basket', False)

        if basket_id and request.user.is_authenticated:
            basket_user, basket_created = Basket.objects.get_or_create(user=request.user)
            basket_session = Basket.objects.get(id=basket_id)

            if not basket_created:
                basket_session = Basket.objects.get(id=basket_id)
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
            return Response({})

        products_in_basket = basket.products.all()
        count_products = dict()

        for product_in_basket in (ProductsInBaskets.objects.filter(basket=basket).values()):
            count_products[product_in_basket['product_id']] = product_in_basket['count']

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

    def post(self, request: Request):
        request_data = request.data
        basket_id: int = request.session.get('basket')

        if request.user.is_authenticated:
            basket, created = Basket.objects.get_or_create(user=request.user)
        else:
            if basket_id:
                basket: Basket = Basket.objects.get(id=basket_id)
            else:
                basket = Basket.objects.create()

        id_product = request_data['id']
        count_product = request_data['count']
        product = Product.objects.get(id=id_product)

        if product.count < request_data['count']:
            count_product = product.count

        products_in_basket = basket.products.all()

        if product not in products_in_basket:
            if product.count > 0:
                basket.products.add(product, through_defaults={'count': count_product})
        else:
            update_product = product.productsinbaskets_set.get(basket=basket, product=product)
            if update_product.count < product.count:
                update_product.count += count_product
            update_product.save()

        products_in_basket = basket.products.all()

        count_products = dict()

        for product_in_basket in (ProductsInBaskets.objects.filter(basket=basket).values()):
            count_products[product_in_basket['product_id']] = product_in_basket['count']

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

    def delete(self, request):
        request_data = json.loads(request.body)
        id_product = request_data['id']
        count_product = request_data['count']
        basket_id = request.session.get('basket')

        if request.user.is_authenticated:
            basket: Basket = Basket.objects.get(user=request.user)
        else:
            if basket_id:
                basket: Basket = Basket.objects.get(id=basket_id)

        product = Product.objects.get(id=id_product)
        product_for_delete = product.productsinbaskets_set.get(basket=basket, product=product)
        product_for_delete.count -= count_product
        product_for_delete.save()

        if product_for_delete.count == 0:
            product_for_delete.delete()

        products_in_basket = basket.products.all()

        count_products = dict()

        for product_in_basket in (ProductsInBaskets.objects.filter(basket=basket).values()):
            count_products[product_in_basket['product_id']] = product_in_basket['count']

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
    serializer_class = OrderSerializer
    queryset = Order.objects.exclude(status__status='Завершён')

    def post(self, request, *args, **kwargs):
        serialized = self.get_serializer(
            data={
                'totalCost': sum([product['price'] * product['count'] for product in request.data]),
            }
        )

        serialized.is_valid(raise_exception=True)
        serialized.save(status=OrderStatus.objects.get(status='На оформлении'))
        return Response({"orderId": serialized.instance.id})


class OrderDetailApiView(RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'

    def get(self, request, id):
        serialized_order = self.get_serializer(Order.objects.get(id=id))
        if request.user.is_authenticated:
            response_data = dict()
            response_data.update(serialized_order.data)
            response_data['fullName'] = str(request.user.userprofile)
            response_data['phone'] = request.user.userprofile.phone
            response_data['email'] = request.user.email
            return Response(response_data)
        return Response(serialized_order.data)

    def post(self, request: Request, *args, **kwargs):
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
    def post(self, request, id):
        order = Order.objects.get(id=id)
        order.status = OrderStatus.objects.get('Оплачен')
        order.save()
        return Response(status=200)


class ProfileApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            data = {
              "fullName": '{last_name} {first_name} {patronymic}'.format(last_name=request.user.last_name,
                                                                         first_name=request.user.first_name,
                                                                         patronymic=request.user.userprofile.patronymic),
              "email": request.user.email,
              "phone": request.user.userprofile.phone,
              "avatar": {
                "src": request.user.useravatar.src.url,
                "alt": "Image alt string"
              }
            }
            return Response(data)
        return Response(status=401)

    def post(self, request):
        if request.user.is_authenticated:
            data_request = request.data

            full_name_list = data_request['fullName'].split()
            last_name, first_name, patronymic = '', '', ''
            if len(full_name_list) == 3:
                last_name, first_name, patronymic = full_name_list
            elif len(full_name_list) == 2:
                last_name, first_name = full_name_list
            elif len(full_name_list) == 1:
                first_name = full_name_list[0]

            user = User.objects.filter(id=request.user.id)
            user_profile = UserProfile.objects.filter(user=request.user)

            user.update(first_name=first_name, last_name=last_name, email=data_request['email'])

            user_profile.update(phone=data_request['phone'], patronymic=patronymic)

            user = User.objects.filter(id=request.user.id)
            user_profile = UserProfile.objects.filter(user=request.user)

            data_response = {
              "fullName": '{last_name} {first_name} {patronymic}'.format(last_name=user[0].last_name,
                                                                         first_name=user[0].first_name,
                                                                         patronymic=user_profile[0].patronymic),
              "email": user[0].email,
              "phone": user_profile[0].phone,
              "avatar": {
                "src": request.user.useravatar.src.url,
                "alt": "Image alt string"
              }
            }
            return Response(data_response)
        return Response(status=401)


class ProfilePasswordApiView(APIView):
    def post(self, request):
        user: User = request.user
        current_password = request.data['passwordCurrent']
        reply_password = request.data['passwordReply']

        if user.check_password(current_password):
            user.set_password(reply_password)
            user.save()
            return Response(status=200)
        return Response(status=401)


class ProfileAvatarApiView(APIView):
    def post(self, request):
        avatar = request.data['avatar']
        user_avatar, created = UserAvatar.objects.update_or_create(
            user=request.user,
            defaults={'src': avatar, 'alt': "Image alt string"}
        )
        data = {
          "src": user_avatar.src.url,
          "alt": "Image alt string"
        }
        return Response(data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


def sign_in(request: Request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        return HttpResponse(status=401)


def sign_out(request: Request):
    logout(request)
    return HttpResponse(status=200)


def sign_up(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['username']
        username = data['username']
        password = data['password']
        user = User(first_name=name, username=username)
        user.set_password(password)
        try:
            user.full_clean()
        except ValidationError:
            return HttpResponse(status=401)
        try:
            user.save()
        except IntegrityError:
            return HttpResponse(status=401)
        user_role = UserRole.objects.get(title='Покупатель')
        UserProfile.objects.create(user=user, role=user_role)
        login(request, user)
        return HttpResponse(status=201)
