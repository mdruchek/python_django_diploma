# Generated by Django 4.2.1 on 2023-06-12 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontend.userrole', verbose_name='Роль пользователя'),
            preserve_default=False,
        ),
    ]