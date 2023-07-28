from django.contrib import admin
from django.contrib.auth.models import User
from .models import (ProductCategory,
                     ProductSubcategory,
                     UserProfile,
                     UserRole,
                     Product,
                     Tag,
                     ImageDepartments,
                     ImagesProducts)


@admin.register(ProductSubcategory)
class ProductSubcategoryAdmin(admin.ModelAdmin):
    pass


class ProductSubcategoryInline(admin.StackedInline):
    model = ProductSubcategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductSubcategoryInline,
    ]


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
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    inlines = [
        ImagesProductInLine,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageDepartments)
class ImageDepartments(admin.ModelAdmin):
    pass


@admin.register(ImagesProducts)
class ImagesProduct(admin.ModelAdmin):
    pass
