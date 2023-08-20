# Generated by Django 4.2.1 on 2023-07-29 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import frontend.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontend', '0020_imagesproducts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('fullname', models.CharField(max_length=100, verbose_name='Полное имя пользователя')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('delivery_type', models.CharField(max_length=20, verbose_name='Тип доставки')),
                ('payment_type', models.CharField(max_length=20, verbose_name='Тип оплаты')),
                ('total_cost', models.FloatField(verbose_name='Полная стоимость')),
                ('city', models.CharField(max_length=50, verbose_name='Город')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50, verbose_name='Статус')),
            ],
        ),
        migrations.AlterModelOptions(
            name='imagedepartments',
            options={'verbose_name': 'Изображение категории товара', 'verbose_name_plural': 'Изображения категорий товара'},
        ),
        migrations.AlterModelOptions(
            name='imagesproducts',
            options={'verbose_name': 'Изображение товара', 'verbose_name_plural': 'Изображения товара'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товар'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'Категория продукта', 'verbose_name_plural': 'Категории товаров'},
        ),
        migrations.AlterModelOptions(
            name='productsubcategory',
            options={'verbose_name': 'Подкатегория товара', 'verbose_name_plural': 'Подкатегории товаров'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Профиль пользователя', 'verbose_name_plural': 'Профили пользователей'},
        ),
        migrations.AlterModelOptions(
            name='userrole',
            options={'verbose_name': 'Роль пользователя', 'verbose_name_plural': 'Роли пользователей'},
        ),
        migrations.AddField(
            model_name='productcategory',
            name='parent',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontend.productcategory', verbose_name='Родительская категория'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imagedepartments',
            name='alt',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='imagedepartments',
            name='src',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Путь'),
        ),
        migrations.AlterField(
            model_name='imagesproducts',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=frontend.models.image_product_directory_path, verbose_name='Фото товара'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='frontend.imagedepartments', verbose_name='Иконка'),
        ),
        migrations.AlterField(
            model_name='productsubcategory',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.productcategory', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Аватарка'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='patronymic',
            field=models.CharField(blank=True, max_length=50, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=12, verbose_name='Номер телефона'),
        ),
        migrations.CreateModel(
            name='ProductsInOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='frontend.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='frontend.product', verbose_name='Товар')),
            ],
        ),
        migrations.CreateModel(
            name='ProductsInBaskets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.ImageField(upload_to='', verbose_name='Количество')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='frontend.basket', verbose_name='Корзина')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='frontend.product', verbose_name='Товар')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='frontend.ProductsInOrders', to='frontend.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='frontend.orderstatus', verbose_name='Статус заказа'),
        ),
        migrations.AddField(
            model_name='basket',
            name='products',
            field=models.ManyToManyField(through='frontend.ProductsInBaskets', to='frontend.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]