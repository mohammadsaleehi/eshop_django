# Generated by Django 4.2.3 on 2023-09-24 20:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0020_alter_articlehit_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlehit',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 24, 23, 44, 5, 700069), verbose_name='تاریخ بازدید'),
        ),
    ]
