# Generated by Django 2.2.7 on 2019-12-27 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role_management', '0008_delete_purchasemanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, unique=True)),
                ('contact_number', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]
