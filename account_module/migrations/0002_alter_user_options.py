# Generated by Django 4.2.3 on 2023-09-23 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-id'], 'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربر ها'},
        ),
    ]
