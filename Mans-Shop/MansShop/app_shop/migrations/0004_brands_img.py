# Generated by Django 3.2.9 on 2022-02-23 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0003_brands'),
    ]

    operations = [
        migrations.AddField(
            model_name='brands',
            name='img',
            field=models.ImageField(default=None, upload_to='brand_photos', verbose_name='Логотип Бренда'),
        ),
    ]
