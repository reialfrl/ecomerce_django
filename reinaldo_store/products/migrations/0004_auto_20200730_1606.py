# Generated by Django 3.0.8 on 2020-07-30 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
