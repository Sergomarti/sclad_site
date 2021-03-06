# Generated by Django 3.0 on 2020-05-30 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200530_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyorders',
            name='order',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.Order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to='users.Product'),
        ),
    ]
