# Generated by Django 2.2.7 on 2019-11-22 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role_management', '0002_auto_20191121_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusercreation',
            name='contact_number',
            field=models.CharField(default=1, max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
