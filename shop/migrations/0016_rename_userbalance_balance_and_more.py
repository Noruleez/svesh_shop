# Generated by Django 4.2.1 on 2023-05-28 04:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0015_purchase_product'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserBalance',
            new_name='Balance',
        ),
        migrations.RenameModel(
            old_name='UserPurchaseLink',
            new_name='PurchaseLink',
        ),
    ]
