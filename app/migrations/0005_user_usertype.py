# Generated by Django 4.2.4 on 2023-08-09 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='usertype',
            field=models.CharField(default='buyer', max_length=100),
        ),
    ]
