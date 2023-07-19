from django.contrib import admin
from .models import (ProductCategory,
                     ProductSubcategory,
                     UserRole,
                     Product,
                     Tag,
                     ImageDepartments,
                     ImagesProducts)


@admin.register(ProductSubcategory)
class ProductSubcategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageDepartments)
class ImageDepartments(admin.ModelAdmin):
    pass


@admin.register(ImagesProducts)
class ImagesProduct(admin.ModelAdmin):
    pass
