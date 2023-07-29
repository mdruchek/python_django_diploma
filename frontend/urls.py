from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers
from .api import (ProductCategoryListView,
                  ProductDetailView,
                  CatalogListView,
                  TagViewSet,
                  ProductLimitedListView,
                  ProductPopularListView,
                  SalesListView,
                  BannersListView,
                  BasketListView,
                  OrderListView,
                  OrderDetailView,
                  PaymentView,
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
    path('api/categories/', ProductCategoryListView.as_view()),
    path('api/product/<int:id>/', ProductDetailView.as_view()),
    path('api/catalog/', CatalogListView.as_view()),
    path('api/products/limited/', ProductLimitedListView.as_view()),
    path('api/products/popular/', ProductPopularListView.as_view()),
    path('api/sales/', SalesListView.as_view()),
    path('api/banners/', BannersListView.as_view()),
    path('api/basket/', BasketListView.as_view()),
    path('api/orders/', OrderListView.as_view()),
    path('api/orders/<int:id>', OrderDetailView.as_view()),
    path('api/payment/', PaymentView.as_view()),
    path('api/sign-in/', sign_in),
    path('api/sign-out/', sign_out),
    path('api/sign-up/', sign_up),
]

urlpatterns += router.urls
