from django.urls import path
from django.views.generic import TemplateView

from rest_framework import routers

from .api import (
    ProductCategoryListApiView,
    ProductDetailApiView,
    ProductReviewApiView,
    CatalogListApiView,
    TagViewSet,
    ProductLimitedListApiView,
    ProductPopularListApiView,
    SalesListApiView,
    BannersListApiView,
    BasketListApiView,
    OrderListApiView,
    OrderDetailApiView,
    PaymentApiView,
)


router = routers.DefaultRouter()
router.register('api/tags', TagViewSet)


urlpatterns = [
    path('api/categories/', ProductCategoryListApiView.as_view()),
    path('api/product/<int:id>/', ProductDetailApiView.as_view()),
    path('api/product/<int:id>/reviews/', ProductReviewApiView.as_view()),
    path('api/catalog/', CatalogListApiView.as_view()),
    path('api/products/limited/', ProductLimitedListApiView.as_view()),
    path('api/products/popular/', ProductPopularListApiView.as_view()),
    path('api/sales/', SalesListApiView.as_view()),
    path('api/banners/', BannersListApiView.as_view()),
    path('api/basket/', BasketListApiView.as_view()),
    path('api/orders/', OrderListApiView.as_view()),
    path('api/order/<int:id>/', OrderDetailApiView.as_view()),
    path('api/payment/<int:id>/', PaymentApiView.as_view()),
]

urlpatterns += router.urls
