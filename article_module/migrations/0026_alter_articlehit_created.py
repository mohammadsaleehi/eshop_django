# Generated by Django 4.2.3 on 2023-10-26 18:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0025_alter_articlehit_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlehit',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 26, 22, 9, 15, 551843), verbose_name='تاریخ بازدید'),
        ),
    ]