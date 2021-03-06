# Generated by Django 3.0 on 2020-05-30 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200530_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionproduct',
            name='was_response',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='was_response',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.Product'),
        ),
    ]
