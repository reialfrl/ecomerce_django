# Generated by Django 3.0.8 on 2020-07-30 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=1, upload_to='products/'),
            preserve_default=False,
        ),
    ]
