# Generated by Django 4.1 on 2022-10-10 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_rest_django', '0018_remove_membership_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='deleted',
            field=models.DateTimeField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='group',
            name='deleted',
            field=models.DateTimeField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='membership',
            name='deleted',
            field=models.DateTimeField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='deleted',
            field=models.DateTimeField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
