# Generated by Django 2.2.7 on 2019-12-19 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('role_management', '0006_modulelist_module_url_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modulelist',
            name='module_url_slug',
        ),
    ]
