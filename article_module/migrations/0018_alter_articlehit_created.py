# Generated by Django 4.2.3 on 2023-09-23 16:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0017_alter_articlehit_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlehit',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 23, 19, 55, 55, 950577), verbose_name='تاریخ بازدید'),
        ),
    ]
