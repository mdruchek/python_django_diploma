from statistics import mean
from rest_framework import serializers
from rest_framework.request import Request
from django.db import transaction
from django.db.models import QuerySet
from .models import (
    ProductCategory,
    ImageDepartments,
    Product,
    ImagesProducts,
    ReviewProduct,
    SpecificationProduct,
    Tag,
    Basket,
    ProductsInBaskets,
    Order,
    ProductsInOrders,
    OrderStatus,
    Sale
)


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


class ImagesProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesProducts
        fields = [
            'src',
            'alt',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
        ]


class ReviewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewProduct
        fields = [
            'author',
            'email',
            'text',
            'rate',
            'date',
        ]


class SpecificationProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationProduct
        fields = [
            'name',
            'value',
        ]


class ProductSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    images = ImagesProductsSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    specifications = SpecificationProductSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'fullDescription',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'specifications',
        ]

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def to_representation(self, instance: Product):
        representations = super().to_representation(instance)
        rate_list = instance.reviews.values_list('rate', flat=True)
        representations['rating'] = round(mean(rate_list), 1) if rate_list else None
        return representations

    def get_reviews(self, product):
        if self.context.get('view').__class__.__name__ == 'ProductDetailApiView':
            return ReviewProductSerializer(product.reviews.all(), many=True).data
        return product.reviews.count()

    def get_count(self, product):
        if self.context.get('count', False):
            return self.context['count'][product.id]
        return product.count


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
            'products',
        ]

    def get_status(self, order):
        return order.status.status

    def get_products(self, order):
        products: QuerySet = order.products.all()
        serialised_products = ProductSerializer(
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
              'reviews'
            ]
        )
        products_in_orders = ProductsInOrders.objects.filter(order_id=order.pk)
        for product in serialised_products.data:
            product['count'] = products_in_orders.get(product_id=product['id']).count
        return serialised_products.data

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        for product in self.context['request'].data:
            ProductsInOrders.objects.create(
                order_id=order.pk,
                product_id=product['id'],
                count=product['count']
            )
        return order

    def update(self, order, validated_data):
        order.fullName = validated_data.get('fullName')
        order.phone = validated_data.get('phone')
        order.email = validated_data.get('email')
        order.deliveryType = validated_data.get('deliveryType')
        order.city = validated_data.get('city')
        order.address = validated_data.get('address')
        order.paymentType = validated_data.get('paymentType')
        order.status = OrderStatus.objects.get(status='Ожидает оплаты')
        order.totalCost = validated_data.get('totalCost')
        order.save()
        return order


class SaleSerializer(serializers.ModelSerializer):
    salePrice = serializers.FloatField(source='sale_price')
    dateFrom = serializers.DateField(source='date_from')
    dateTo = serializers.DateField(source='date_to')

    class Meta:
        model = Sale
        fields = [
            'salePrice',
            'dateFrom',
            'dateTo'
        ]

    def to_representation(self, sale):
        representations = super().to_representation(sale)
        representations['id'] = sale.product.pk
        representations['price'] = sale.product.price
        representations['title'] = sale.product.title
        representations['images'] = ImagesProductsSerializer(sale.product.images, many=True).data
        return representations
