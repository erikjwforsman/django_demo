# Generated by Django 3.0.6 on 2020-07-29 07:55

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200728_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=account.models.upload_location),
        ),
    ]
