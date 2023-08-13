import os
from pathlib import Path, PurePath
from io import TextIOWrapper
from csv import DictReader

from django.core.files.images import ImageFile
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.core.files import File

import settings.settings
from .models import (ProductCategory,
                     UserProfile,
                     UserRole,
                     Product,
                     Tag,
                     ImageDepartments,
                     ImagesProducts)
from .forms import CSVImportForms
from .admin_mixins import ExportAsCSVMixin


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_full_name']

    @admin.display(ordering='user__username', description='ФИО')
    def user_full_name(self, obj):
        return '{first_name} {last_name}'.format(first_name=obj.user.first_name, last_name=obj.user.last_name)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass


class ImagesProductInLine(admin.StackedInline):
    model = ImagesProducts


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "frontend/products_changelist.html"
    actions = [
        'export_csv',
    ]
    list_display = ['title', 'price']
    inlines = [
        ImagesProductInLine,
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
            default_icon = Path(PurePath(settings.settings.MEDIA_ROOT, 'img','products', 'default_icon_product.jpg'))

            img_product: ImagesProducts = ImagesProducts.objects.create()

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
class ImageDepartments(admin.ModelAdmin):
    pass


@admin.register(ImagesProducts)
class ImagesProduct(admin.ModelAdmin):
    pass
