from typing import Dict

from django.contrib.auth.models import User

from rest_framework import serializers

from .models import (
    UserProfile,
    UserAvatar
)


class UserAvatarSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели UserAvatar
    """

    class Meta:
        model = UserAvatar
        fields = [
            'src',
            'alt'
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели UserProfile
    """

    fullName = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField(validators=[])
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'fullName',
            'email',
            'phone',
            'avatar'
        ]

    def get_fullName(self, user: User):
        """
        Возвращает полное имя пользователя
        """
        return '%s %s %s' % (user.last_name, user.first_name, user.userprofile.patronymic)

    def get_phone(self, user: User) -> str:
        """
        Возвращает телефон пользователя
        """
        return user.userprofile.phone

    def get_avatar(self, user: User) -> Dict:
        """
        Возвращает данные аватара пользователя
        """
        return UserAvatarSerializer(user.useravatar).data

    def update(self, user: User, validated_data):
        request_data = self.context['request'].data
        full_name: str = request_data['fullName'].split()

        last_name, first_name, patronymic = [full_name[index]
                                             if index < len(full_name)
                                             else ''
                                             for index in range(3)]

        user.last_name = last_name
        user.first_name = first_name
        user.email = validated_data.get('email', user.email)
        user.save()

        profile: UserProfile = UserProfile.objects.get(user=user)
        profile.phone = request_data['phone']
        profile.patronymic = patronymic
        profile.save()

        return user
