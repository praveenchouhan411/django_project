# Generated by Django 2.2.7 on 2020-02-28 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role_management', '0011_delete_moduleslug'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.CharField(max_length=200, unique=True)),
                ('ip_address', models.CharField(max_length=200, unique=True)),
                ('status', models.IntegerField(unique=True)),
                ('loggedin_by', models.IntegerField(null=True)),
                ('loggedin_at', models.DateTimeField(null=True)),
            ],
        ),
    ]
