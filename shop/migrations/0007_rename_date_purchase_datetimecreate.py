# Generated by Django 4.2.1 on 2023-05-27 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_purchase_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='date',
            new_name='datetimecreate',
        ),
    ]