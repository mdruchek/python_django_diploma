import json

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.http import HttpRequest, HttpResponse
from .serializers import (TagSerializer)
from .models import (ProductCategory,
                     Product,
                     Tag)
import re


class ProductCategoryListView(APIView):
    def get(self, request):
        categories = ProductCategory.objects.all()
        data = [{"id": category.id,
                 "title": category.title,
                 "image": {
                     "src": category.image.src,
                     "alt": category.image.alt
                 },
                 "subcategories": [{"id": subcategory.id,
                                    "title": subcategory.title,
                                    "image": {
                                        "src": "/static/frontend/assets/img/icons/departments/1.svg",
                                        "alt": "Image alt string"
                                    }} for subcategory in category.productsubcategory_set.all()]} for category in
                categories]
        return Response(data)


class ProductDetailView(APIView):
    def get(self, request, id):
        product = Product.objects.get(id=id)
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
            "images": [{'src': re.search(r'/static/.*', image.image.path).group(),
                        'alt': "Image alt string"} for image in product.imagesproducts_set.all()],
            "tags": [
                "string"
            ],
            "reviews": [
                {
                    "author": "Annoying Orange",
                    "email": "no-reply@mail.ru",
                    "text": "rewrewrwerewrwerwerewrwerwer",
                    "rate": 4,
                    "date": "2023-05-05 12:12"
                }
            ],
            "specifications": [
                {
                    "name": "Size",
                    "value": "XL"
                }
            ],
            "rating": 4.6
        }
        return Response(data)


class CatalogListView(APIView):
    def get(self, request):
        products = Product.objects.all()
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
                "images": [{'src': re.search(r'/static/.*', image.image.path).group(),
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


class ProductLimitedListView(APIView):
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
            "images": [{'src': re.search(r'/static/.*', image.image.path).group(),
                        'alt': "Image alt string"} for image in product.imagesproducts_set.all()],
            "tags": [{
                "id": tag.id,
                "name": tag.name
            } for tag in product.tags.all()],
            "reviews": 5,
            "rating": 4.6
        } for product in products]
        return Response(data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


def sign_in(request: Request):
    data = json.loads(request.body)
    print(data)
    return HttpResponse('')
