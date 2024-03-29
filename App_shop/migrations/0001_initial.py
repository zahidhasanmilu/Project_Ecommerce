# Generated by Django 5.0.1 on 2024-01-29 02:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=300, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='Category_Images/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='App_shop.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': '',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=300, unique=True)),
                ('image', models.ImageField(upload_to='Product_Images/')),
                ('preview_description', models.TextField(blank=True, null=True)),
                ('full_description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(default=0.0)),
                ('old_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('is_stock', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_product', to='App_shop.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': '',
                'managed': True,
            },
        ),
    ]
