# Generated by Django 4.2.3 on 2023-09-20 22:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0008_alter_producthit_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producthit',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 21, 1, 39, 45, 700960), verbose_name='زمان مشاهده'),
        ),
    ]
