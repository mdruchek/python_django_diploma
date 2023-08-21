from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers
from .api import (ProductCategoryListApiView,
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
                  ProfileApiView,
                  ProfilePasswordApiView,
                  ProfileAvatarApiView,
                  sign_in,
                  sign_out,
                  sign_up)


router = routers.DefaultRouter()
router.register('api/tags', TagViewSet)


urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/index.html")),
    path('about/', TemplateView.as_view(template_name="frontend/about.html")),
    path('account/', TemplateView.as_view(template_name="frontend/account.html")),
    path('cart/', TemplateView.as_view(template_name="frontend/cart.html")),
    path('catalog/', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('catalog/<int:id>/', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('history-order/', TemplateView.as_view(template_name="frontend/historyorder.html")),
    path('order-detail/<int:id>/', TemplateView.as_view(template_name="frontend/oneorder.html")),
    path('orders/<int:id>/', TemplateView.as_view(template_name="frontend/order.html")),
    path('payment/<int:id>/', TemplateView.as_view(template_name="frontend/payment.html")),
    path('payment-someone/', TemplateView.as_view(template_name="frontend/paymentsomeone.html")),
    path('product/<int:id>/', TemplateView.as_view(template_name="frontend/product.html")),
    path('profile/', TemplateView.as_view(template_name="frontend/profile.html")),
    path('progress-payment/', TemplateView.as_view(template_name="frontend/progressPayment.html")),
    path('sale/', TemplateView.as_view(template_name="frontend/sale.html")),
    path('sign-in/', TemplateView.as_view(template_name="frontend/signIn.html")),
    path('sign-up/', TemplateView.as_view(template_name="frontend/signUp.html")),
    path('api/categories/', ProductCategoryListApiView.as_view()),
    path('api/product/<int:id>/', ProductDetailApiView.as_view()),
    path('api/product/<int:id>/review/', ProductReviewApiView.as_view()),
    path('api/catalog/', CatalogListApiView.as_view()),
    path('api/products/limited/', ProductLimitedListApiView.as_view()),
    path('api/products/popular/', ProductPopularListApiView.as_view()),
    path('api/sales/', SalesListApiView.as_view()),
    path('api/banners/', BannersListApiView.as_view()),
    path('api/basket/', BasketListApiView.as_view()),
    path('api/orders/', OrderListApiView.as_view()),
    path('api/orders/<int:id>', OrderDetailApiView.as_view()),
    path('api/payment/', PaymentApiView.as_view()),
    path('api/profile/', ProfileApiView.as_view()),
    path('api/profile/password/', ProfilePasswordApiView.as_view()),
    path('api/profile/avatar/', ProfileAvatarApiView.as_view()),
    path('api/sign-in/', sign_in),
    path('api/sign-out/', sign_out),
    path('api/sign-up/', sign_up),
]

urlpatterns += router.urls
