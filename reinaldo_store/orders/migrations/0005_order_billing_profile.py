# Generated by Django 3.0.8 on 2020-08-21 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing_profiles', '0001_initial'),
        ('orders', '0004_order_promo_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing_profiles.BillingProfile'),
        ),
    ]
