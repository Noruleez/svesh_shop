# Generated by Django 4.2.1 on 2023-05-27 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_userbalance_balance'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserPurchaseLinks',
            new_name='ProductLink',
        ),
        migrations.RemoveField(
            model_name='productlink',
            name='purchase',
        ),
        migrations.AddField(
            model_name='productlink',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userpurchase',
            name='amount',
            field=models.IntegerField(db_index=True, default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserPurchaseLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(db_index=True, max_length=150)),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.userpurchase')),
            ],
        ),
    ]
