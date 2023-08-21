import json
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.admin import User
from django.db import IntegrityError
from django.db.models import Avg
from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import (TagSerializer, ProductCategorySerializer)
from .models import (UserProfile,
                     UserAvatar,
                     UserRole,
                     ProductCategory,
                     Product,
                     ReviewProduct,
                     Tag)


class ProductCategoryListApiView(ListAPIView):
    queryset = ProductCategory.objects.filter(parent__isnull=True)
    serializer_class = ProductCategorySerializer


class ProductDetailApiView(APIView):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        reviews_product = ReviewProduct.objects.filter(product=product)
        data = {
            "id": product.id,
            "category": product.category.id,
            "price": product.price,
            "count": product.count,
            "date": product.date,
            "title": product.title,
            "description": product.description,
            "fullDescription": product.fullDescription,
            "freeDelivery": product.freeDelivery,
            "images": [{'src': image.image.url,
                        'alt': "Image alt string"} for image in product.imagesproducts_set.all()],
            "tags": [{
                    "id": tag.id,
                    "name": tag.name
            } for tag in product.tags.all()],
            "reviews": [
                {
                    "author": review.author,
                    "email": review.email,
                    "text": review.text,
                    "rate": review.rate,
                    "date": review.created_to
                } for review in reviews_product],
            "specifications": [
                {
                    "name": specification.name,
                    "value": specification.value
                } for specification in product.specifications],
            "rating": reviews_product.aggregate(Avg('rate'))
        }
        return Response(data)


class CatalogListApiView(APIView):
    def get(self, request):
        parameters = json.loads(request.body)

        if parameters['available']:
            products = Product.objects.filter(title__contains=parameters['name'],
                                              price__gte=parameters['minPrice'],
                                              price__lte=parameters['maxPrice'],
                                              freeDelivery=parameters['freeDelivery'],
                                              count__gt=0)
        else:
            products = Product.objects.filter(title__contains=parameters['name'],
                                              price__gte=parameters['minPrice'],
                                              price__lte=parameters['maxPrice'],
                                              freeDelivery=parameters['freeDelivery'])

        data = {
            "items": [{
                "id": product.id,
                "category": product.category.id,
                "price": product.price,
                "count": product.count,
                "date": product.date,
                "title": product.title,
                "description": product.description,
                "freeDelivery": product.freeDelivery,
                "images": [{'src': image.image.url,
                            'alt': "Image alt string"} for image in product.imagesproducts_set.all()],
                "tags": [{
                    "id": tag.id,
                    "name": tag.name
                } for tag in product.tags.all()],
                "reviews": 5,
                "rating": 4.6
            } for product in products],
            "currentPage": 1,
            "lastPage": 1
        }
        return Response(data)


class ProductLimitedListApiView(APIView):
    def get(self, request):
        products = Product.objects.filter(count__lte=5)
        data = [{
            "id": product.id,
            "category": product.category.id,
            "price": product.price,
            "count": product.count,
            "date": product.date,
            "title": product.title,
            "description": product.description,
            "freeDelivery": product.freeDelivery,
            "images": [{'src': image.image.url,
                        'alt': "Image alt string"} for image in product.imagesproducts_set.all()],
            "tags": [{
                "id": tag.id,
                "name": tag.name
            } for tag in product.tags.all()],
            "reviews": 5,
            "rating": 4.6
        } for product in products]
        return Response(data)


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
    def get(self, request):
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

    def post(self, request):
        request_data = json.loads(request.body)
        id_product = request_data['id']
        count_product = request_data['count']
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

    def delete(self, request):
        request_data = json.loads(request.body)
        id_product = request_data['id']
        count_product = request_data['count']
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


class OrderListApiView(APIView):
    def get(self, request):
        data = [{
            "id": 123,
            "createdAt": "2023-05-05 12:12",
            "fullName": "Annoying Orange",
            "email": "no-reply@mail.ru",
            "phone": "88002000600",
            "deliveryType": "free",
            "paymentType": "online",
            "totalCost": 567.8,
            "status": "accepted",
            "city": "Moscow",
            "address": "red square 1",
            "products": [
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
        }]
        return Response(data)

    def post(self, request):
        request_data = json.loads(request.body)
        order_id = request_data['orderId']
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


class OrderDetailApiView(APIView):
    def get(self, request, id):
        data = {
          "id": 123,
          "createdAt": "2023-05-05 12:12",
          "fullName": "Annoying Orange",
          "email": "no-reply@mail.ru",
          "phone": "88002000600",
          "deliveryType": "free",
          "paymentType": "online",
          "totalCost": 567.8,
          "status": "accepted",
          "city": "Moscow",
          "address": "red square 1",
          "products": [
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
        }
        return Response(data)

    def post(self, id):
        data = {
          "id": 123,
          "createdAt": "2023-05-05 12:12",
          "fullName": "Annoying Orange",
          "email": "no-reply@mail.ru",
          "phone": "88002000600",
          "deliveryType": "free",
          "paymentType": "online",
          "totalCost": 567.8,
          "status": "accepted",
          "city": "Moscow",
          "address": "red square 1",
          "products": [
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
        }
        return Response(data)


class PaymentApiView(APIView):
    def post(self, request):
        pass


class ProfileApiView(APIView):
    def get(self, request):
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

    def post(self, request):
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


class ProfilePasswordApiView(APIView):
    def post(self, request):
        return Response('')


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
        return HttpResponse(status=404)


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
