# Generated by Django 4.2.1 on 2023-05-27 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_rename_date_purchase_datetimecreate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='datetimecreate',
            new_name='date_time_create',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='link',
        ),
        migrations.CreateModel(
            name='PurchaseLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(db_index=True, max_length=150)),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.purchase')),
            ],
        ),
    ]
