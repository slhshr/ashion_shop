# Generated by Django 4.2.7 on 2023-11-09 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_customer_alter_order_customer_and_more'),
        ('account', '0002_alter_customer_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
