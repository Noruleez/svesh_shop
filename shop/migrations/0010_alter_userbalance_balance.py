# Generated by Django 4.2.1 on 2023-05-27 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_rename_purchase_userpurchase_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbalance',
            name='balance',
            field=models.IntegerField(db_index=True),
        ),
    ]