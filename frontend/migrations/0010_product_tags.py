# Generated by Django 4.2.1 on 2023-06-13 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0009_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='frontend.tag', verbose_name='Tags'),
        ),
    ]