# Generated by Django 3.1.2 on 2021-09-22 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pitbull', '0004_user_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='admin',
        ),
    ]