# Generated by Django 4.1 on 2022-10-06 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_rest_django', '0015_group_membership_group_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='group',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='person',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
    ]
