from pathlib import Path, PurePath
from io import TextIOWrapper
from csv import DictReader
from typing import List

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.core.files import File

import settings.settings
from .models import (
    ProductCategory,
    Product,
    SpecificationProduct,
    Tag,
    ImagesProducts,
    Basket,
    OrderStatus,
    Sale
)

from .forms import CSVImportForms
from .admin_mixins import ExportAsCSVMixin


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """
    Класс администрирования категории товара
    """

    list_display = [
        'title', 'is_active'
    ]


class ImagesProductInLine(admin.StackedInline):
    """
    Класс внедрения изображения товара
    """

    model = ImagesProducts


class SpecificationProductInLine(admin.StackedInline):
    """
    Класс внедрения спецификации товара
    """

    model = SpecificationProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    """
    Класс администрирования товара
    """

    change_list_template = "frontend/products_changelist.html"
    actions = [
        'export_csv',
    ]
    list_display = ['title', 'count', 'price', 'date']
    inlines = [
        ImagesProductInLine,
        SpecificationProductInLine
    ]

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        """
        Метод импортирования товаров из csv файла
        """

        if request.method == 'GET':
            form = CSVImportForms

            context: dict = {
                'form': form
            }

            return render(request, 'admin/csv_form.html', context)

        form = CSVImportForms(request.POST, request.FILES)

        if not form.is_valid():

            context: dict = {
                'form': form
            }

            return render(request, 'admin/csv_form.html', context, status=400)

        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding='utf-8',
        )

        reader = DictReader(csv_file)

        products: list = [
            self.replacing_product_category_with_an_object(**row)
            for row in reader
        ]

        products: QuerySet = Product.objects.bulk_create(products)

        for product in products:
            default_icon: Path = Path(PurePath(settings.settings.MEDIA_ROOT, 'img', 'products', 'default_icon_product.jpg'))

            img_product: ImagesProducts = ImagesProducts()

            with default_icon.open(mode='rb') as f:
                img_product.image = File(f, name=default_icon.name)
                img_product.product = product
                img_product.save()

        self.message_user(request, message="Данные из CSV загружены.")
        return redirect('..')

    def get_urls(self) -> List[path]:
        """
        Метод добавления URL
        """

        urls = super().get_urls()

        new_urls: list = [
            path(
                'import-products-csv/',
                self.import_csv,
                name='import_products_csv'
            ),
        ]

        return new_urls + urls

    def replacing_product_category_with_an_object(self, **row) -> Product:
        """
        Замена категории товара на объект ProductCategory
        """

        row['category'] = ProductCategory.objects.get(title=row['category'])
        return Product(**row)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Класс администрирования тэгов товара
    """
    pass


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """
    Класс администрирования корзины
    """

    list_display = [
        "username"
    ]

    @admin.display(empty_value="Аноним")
    def username(self, obj: Basket) -> str:
        if obj.user:
            username = obj.user.username
            return f" Корзина {username}"
        return "Корзина анонима"


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    """
    Класс администрирования заказа
    """
    pass


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Класс администрирования скидок
    """

    list_display = [
        'product',
        'product_price',
        'sale_price',
        'date_from',
        'date_to'
    ]

    @admin.display(description='Цена без скидки')
    def product_price(self, obj):
        """
        Отображение стоимости товара в общей таблице
        """

        return obj.product.price

