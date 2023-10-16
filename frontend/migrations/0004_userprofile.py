# Generated by Django 4.2.1 on 2023-06-12 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_userrole'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patronymic', models.CharField(max_length=50, verbose_name='Отчество')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('avatar', models.ImageField(upload_to='', verbose_name='Аватарка')),
            ],
        ),
    ]
