from rest_framework import viewsets
from .serializers import (ProductCategorySerializer,
                          ProductSubcategorySerializer,
                          ProductSerializer,
                          TagSerializer)
from .models import (ProductCategory,
                     ProductSubcategory,
                     Product,
                     Tag)


class ProductSubcategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductSubcategory.objects.all()
    serializer_class = ProductSubcategorySerializer


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
