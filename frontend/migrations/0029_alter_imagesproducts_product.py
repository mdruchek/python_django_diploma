# Generated by Django 4.2.1 on 2023-07-31 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0028_alter_imagesproducts_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesproducts',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.product', verbose_name='Товар'),
        ),
    ]
