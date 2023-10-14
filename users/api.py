import json

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated


from .models import (
    UserAvatar,
    UserProfile
)


from .serializers import (
    UserSerializer
)


class ProfileApiView(RetrieveAPIView, UpdateModelMixin):
    """
    ApiView для отображения и изменения профиля
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self):
        return self.request.user

    def post(self, request: Request) -> Response:
        return self.update(request)


class ProfilePasswordApiView(APIView):
    """
    ApiView для изменения пароля
    """
    def post(self, request: Request) -> Response:
        user: User = request.user
        current_password = request.data['passwordCurrent']
        reply_password = request.data['passwordReply']

        if user.check_password(current_password):
            user.set_password(reply_password)
            user.save()
            return Response(status=200)
        return Response(status=401)


class ProfileAvatarApiView(APIView):
    """
    ApiView для изменения аватарки
    """
    def post(self, request: Request) -> Response:
        avatar = request.data['avatar']
        user_avatar, created = UserAvatar.objects.update_or_create(
            user=request.user,
            defaults={'src': avatar, 'alt': "Image alt string"}
        )
        data = {
          "src": user_avatar.src.url,
          "alt": "Image alt string"
        }
        return Response(data)