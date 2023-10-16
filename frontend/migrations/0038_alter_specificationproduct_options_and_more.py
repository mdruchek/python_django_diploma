# Generated by Django 4.2.1 on 2023-09-27 18:06

from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0037_specificationproduct'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specificationproduct',
            options={'verbose_name': 'Характеристика товара', 'verbose_name_plural': 'Характеристики товаров'},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='created_at',
            new_name='createdAt',
        ),
        migrations.RenameField(
            model_name='reviewproduct',
            old_name='created_to',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='imagesproducts',
            name='image',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_type',
        ),
        migrations.RemoveField(
            model_name='order',
            name='fullname',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_type',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_cost',
        ),
        migrations.AddField(
            model_name='imagesproducts',
            name='alt',
            field=models.CharField(default='Image alt string', max_length=50, verbose_name='описание'),
        ),
        migrations.AddField(
            model_name='imagesproducts',
            name='src',
            field=models.ImageField(default='img/products/default_icon_product.jpg', upload_to=shop.models.image_product_directory_path, verbose_name='Фото товара'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='deliveryType',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Тип доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='paymentType',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Тип оплаты'),
        ),
        migrations.AddField(
            model_name='order',
            name='totalCost',
            field=models.FloatField(blank=True, null=True, verbose_name='Полная стоимость'),
        ),
        migrations.AddField(
            model_name='product',
            name='limited_edition',
            field=models.BooleanField(default=False, verbose_name='Ограниченный тираж'),
        ),
        migrations.AlterField(
            model_name='imagesproducts',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='frontend.product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='productsinbaskets',
            name='count',
            field=models.IntegerField(verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='reviewproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='frontend.product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='specificationproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='frontend.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='order',
            name='fullName',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Полное имя пользователя'),
        ),
    ]
