import json

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated


from .models import (
    UserAvatar,
    UserProfile
)


from .serializers import (
    UserSerializer,
    UserAvatarSerializer
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


class ProfileAvatarApiView(RetrieveUpdateAPIView):
    """
    ApiView для изменения аватарки
    """

    serializer_class = UserAvatarSerializer
    queryset = UserAvatar.objects.all()

    def post(self, request):
        avatar = self.get_queryset().get(user=request.user)

        serializer = UserAvatarSerializer(
            avatar,
            data={
                'src': request.data['avatar'],
                'alt': 'Image alt string'
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data)
