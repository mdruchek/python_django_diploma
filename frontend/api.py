from rest_framework import viewsets
from  rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (ProductCategorySerializer,
                          ProductSubcategorySerializer,
                          ProductSerializer,
                          TagSerializer)
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


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.select_related('subcategories').all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductLimitedViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(count__lt=10)
    serializer_class = ProductSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
