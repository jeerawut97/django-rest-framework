# Generated by Django 4.1 on 2022-10-05 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_rest_django', '0008_personalinformation_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalinformation',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='personalinformation',
            name='last_name',
        ),
    ]