# Generated by Django 4.1 on 2022-10-06 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_rest_django', '0017_group_membership_group_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='date_joined',
        ),
    ]
