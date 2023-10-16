from django.urls import path

from .views import (
    sign_in,
    sign_out,
    sign_up
)

from .api import (
    ProfileApiView,
    ProfilePasswordApiView,
    ProfileAvatarApiView
)


urlpatterns = [
    path('api/profile/', ProfileApiView.as_view()),
    path('api/profile/password/', ProfilePasswordApiView.as_view()),
    path('api/profile/avatar/', ProfileAvatarApiView.as_view()),
    path('api/sign-in/', sign_in),
    path('api/sign-out/', sign_out),
    path('api/sign-up/', sign_up)
]
