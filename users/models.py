from django.db import models
from django.contrib.auth.models import User


class UserRole(models.Model):
    title = models.CharField(max_length=100, verbose_name='Роль пользователя')

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
        db_table = 'frontend_userrole'

    def __str__(self):
        return self.title


class UserAvatar(models.Model):
    src = models.ImageField(verbose_name='Аватар')
    alt = models.CharField(verbose_name='Описание', max_length=50, default='User avatar')
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Аватарка пользователя'
        verbose_name_plural = 'Аватарки пользователей'
        db_table = 'frontend_useravatar'


class UserProfile(models.Model):
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', blank=True)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, verbose_name='Роль пользователя')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        db_table = 'frontend_userprofile'

    def __str__(self):
        return '{last_name} {fist_name} {patronymic}'.format(patronymic=self.patronymic,
                                                             fist_name=self.user.first_name,
                                                             last_name=self.user.last_name)
