from django.contrib import admin
from .models import (ProductCategory,
                     UserRole)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass
