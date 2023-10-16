from pathlib import Path, PurePath
from io import TextIOWrapper
from csv import DictReader

from django.contrib import admin
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
    ImageDepartments,
    ImagesProducts,
    Basket,
    OrderStatus,
    Sale
)

from .forms import CSVImportForms
from .admin_mixins import ExportAsCSVMixin


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


class ImagesProductInLine(admin.StackedInline):
    model = ImagesProducts


class SpecificationProductInLine(admin.StackedInline):
    model = SpecificationProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
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
        if request.method == 'GET':
            form = CSVImportForms
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForms(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html', context, status=400)

        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding='utf-8',
        )
        reader = DictReader(csv_file)

        products = [
            self.replacing_product_category_with_an_object(**row)
            for row in reader
        ]
        products = Product.objects.bulk_create(products)

        for product in products:
            default_icon = Path(PurePath(settings.settings.MEDIA_ROOT, 'img', 'products', 'default_icon_product.jpg'))

            img_product: ImagesProducts = ImagesProducts()

            with default_icon.open(mode='rb') as f:
                img_product.image = File(f, name=default_icon.name)
                img_product.product = product
                img_product.save()

        self.message_user(request, message="Данные из CSV загружены.")
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-products-csv/',
                 self.import_csv,
                 name='import_products_csv'
            ),
        ]
        return new_urls + urls

    def replacing_product_category_with_an_object(self, **row):
        row['category'] = ProductCategory.objects.get(title=row['category'])
        return Product(**row)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageDepartments)
class ImageDepartmentsAdmin(admin.ModelAdmin):
    pass


@admin.register(ImagesProducts)
class ImagesProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'product_price',
        'sale_price',
        'date_from',
        'date_to'
    ]

    @admin.display(description='Цена без скидки')
    def product_price(self, obj):
        return obj.product.price

