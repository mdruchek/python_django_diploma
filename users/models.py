from django.db import models
from django.contrib.auth.models import User


class UserRole(models.Model):
    title = models.CharField(verbose_name='роль пользователя', max_length=100)

    class Meta:
        verbose_name = 'роль пользователя'
        verbose_name_plural = 'роли пользователей'
        db_table = 'frontend_userrole'

    def __str__(self):
        return self.title


def image_product_directory_path(instance: 'UserAvatar', filename: str) -> str:
    return 'img/users_avatars/user_{pk}/{filename}'.format(pk=instance.user.pk, filename=filename)


class UserAvatar(models.Model):
    src = models.ImageField(verbose_name='аватар', upload_to=image_product_directory_path, blank=True, null=True)
    alt = models.CharField(verbose_name='описание', max_length=50, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'аватарка пользователя'
        verbose_name_plural = 'аватарки пользователей'
        db_table = 'frontend_useravatar'


class UserProfile(models.Model):
    patronymic = models.CharField(verbose_name='отчество', max_length=50, blank=True, null=True)
    phone = models.CharField(verbose_name='номер телефона', max_length=12, blank=True, null=True)
    user = models.OneToOneField(User, verbose_name='пользователь', on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole, verbose_name='роль пользователя', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'
        db_table = 'frontend_userprofile'

    def __str__(self):
        return '{last_name} {fist_name} {patronymic}'.format(patronymic=self.patronymic,
                                                             fist_name=self.user.first_name,
                                                             last_name=self.user.last_name)