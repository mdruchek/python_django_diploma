from rest_framework import serializers
from .models import (ProductCategory,
                     ImageDepartments,
                     Product,
                     Tag)


class ImageDepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageDepartments
        fields = ['src', 'alt']


class ProductCategorySerializer(serializers.ModelSerializer):
    image = ImageDepartmentsSerializer(read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'title', 'image', 'subcategories']

    def to_representation(self, instance):
        self.fields['subcategories'] = ProductCategorySerializer(many=True, read_only=True)
        return super(ProductCategorySerializer, self).to_representation(instance)


# class ProductSubcategorySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ProductSubcategory
#         fields = ['id', 'title']
#
#
# class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ProductCategory
#         fields = ['id', 'title', 'subcategories']


# class ProductSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id',
#                   'category',
#                   'price',
#                   'count',
#                   'date',
#                   'title',
#                   'description',
#                   'fullDescription',
#                   'freeDelivery',
#                   'tags']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
