# Generated by Django 4.2.3 on 2023-10-26 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_module', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ipaddress',
            name='user',
        ),
    ]
