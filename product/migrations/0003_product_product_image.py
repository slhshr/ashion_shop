# Generated by Django 4.2.7 on 2023-11-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_remove_order_status_shippingaddress_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]