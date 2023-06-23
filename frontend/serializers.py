from rest_framework import serializers
from .models import (ProductCategory,
                     ProductSubcategory,
                     Product,
                     Tag)


class ProductSubcategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductSubcategory
        fields = ['id', 'title']


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'title', 'subcategories']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'price', 'count', 'date', 'title', 'category']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
