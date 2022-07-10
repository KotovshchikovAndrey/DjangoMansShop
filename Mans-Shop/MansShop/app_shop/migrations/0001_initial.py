# Generated by Django 3.2.9 on 2022-02-22 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название Категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название Товара')),
                ('description', models.TextField(verbose_name='Описание Товара')),
                ('price', models.DecimalField(decimal_places=3, default=0, max_digits=10, verbose_name='Цена Товара')),
                ('photo', models.ImageField(upload_to='product_photos', verbose_name='Фото Товара')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shop.category', verbose_name='Категория Товара')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_photos', verbose_name='Фото Товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shop.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
            },
        ),
    ]