from django.contrib import admin

from .models import (
    UserProfile,
    UserRole,
    UserAvatar
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Класс администрирования профиля пользователя
    """

    list_display = ['user', 'user_full_name']

    @admin.display(ordering='user__username', description='ФИО')
    def user_full_name(self, obj):
        return '{first_name} {last_name}'.format(first_name=obj.user.first_name, last_name=obj.user.last_name)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    Класс администрирования роли пользователя
    """

    pass


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    """
    Класс администрирования аватарки пользователя
    """

    pass
