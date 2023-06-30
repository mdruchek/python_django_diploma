from rest_framework import viewsets
from  rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (TagSerializer)
from .models import (ProductCategory,
                     ProductSubcategory,
                     Product,
                     Tag)


class ProductCategoryListView(APIView):
    def get(self, request):
        categories = ProductCategory.objects.all()
        data = [{"id": category.id,
                 "title": category.title,
                 "subcategories": [{"id": subcategory.id,
                                    "title": subcategory.title} for subcategory in category.productsubcategory_set.all()]} for category in categories]
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
            "freeDelivery": product.freeDelivery
        }
        return Response(data)


class CatalogListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = {
            "items": [{"id": product.id,
                        "category": product.category.id,
                        "price": product.price,
                        "count": product.count,
                        "date": product.date,
                        "title": product.title,
                        "description": product.description,
                        "freeDelivery": product.freeDelivery,
                        "tags": [{"id": tag.id,
                                  "name": tag.name} for tag in product.tags]} for product in products],
            "currentPage": 1,
            "lastPage": 1
        }
        return Response(data)


# class ProductCategoryViewSet(viewsets.ModelViewSet):
#     queryset = ProductCategory.objects.select_related('subcategories').all()
#     serializer_class = ProductCategorySerializer


# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductLimitedViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.filter(count__lt=10)
#     serializer_class = ProductSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
