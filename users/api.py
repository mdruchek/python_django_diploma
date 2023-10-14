from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from .models import (
    UserAvatar,
    UserProfile
)


class ProfileApiView(APIView):
    """
    ApiView для отображения и изменения профиля
    """
    def get(self, request: Request) -> Response:
        if request.user.is_authenticated:
            data = {
              "fullName": '{last_name} {first_name} {patronymic}'.format(last_name=request.user.last_name,
                                                                         first_name=request.user.first_name,
                                                                         patronymic=request.user.userprofile.patronymic),
              "email": request.user.email,
              "phone": request.user.userprofile.phone,
              "avatar": {
                "src": request.user.useravatar.src.url,
                "alt": "Image alt string"
              }
            }
            return Response(data)
        return Response(status=401)

    def post(self, request: Request) -> Response:
        if request.user.is_authenticated:
            data_request = request.data

            full_name_list = data_request['fullName'].split()
            last_name, first_name, patronymic = '', '', ''
            if len(full_name_list) == 3:
                last_name, first_name, patronymic = full_name_list
            elif len(full_name_list) == 2:
                last_name, first_name = full_name_list
            elif len(full_name_list) == 1:
                first_name = full_name_list[0]

            user = User.objects.filter(id=request.user.id)
            user_profile = UserProfile.objects.filter(user=request.user)

            user.update(first_name=first_name, last_name=last_name, email=data_request['email'])

            user_profile.update(phone=data_request['phone'], patronymic=patronymic)

            user = User.objects.filter(id=request.user.id)
            user_profile = UserProfile.objects.filter(user=request.user)

            data_response = {
              "fullName": '{last_name} {first_name} {patronymic}'.format(last_name=user[0].last_name,
                                                                         first_name=user[0].first_name,
                                                                         patronymic=user_profile[0].patronymic),
              "email": user[0].email,
              "phone": user_profile[0].phone,
              "avatar": {
                "src": request.user.useravatar.src.url,
                "alt": "Image alt string"
              }
            }
            return Response(data_response)
        return Response(status=401)


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