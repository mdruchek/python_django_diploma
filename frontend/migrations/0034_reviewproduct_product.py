# Generated by Django 4.2.1 on 2023-08-21 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0033_reviewproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewproduct',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='frontend.product', verbose_name='Товар'),
            preserve_default=False,
        ),
    ]
