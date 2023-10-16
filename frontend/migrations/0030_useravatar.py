# Generated by Django 4.2.1 on 2023-08-17 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0029_alter_imagesproducts_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.ImageField(upload_to='', verbose_name='Аватар')),
                ('alt', models.CharField(default='User avatar', max_length=50, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Аватарка пользователя',
                'verbose_name_plural': 'Аватарки пользователей',
            },
        ),
    ]
