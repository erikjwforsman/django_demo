# Generated by Django 3.0.6 on 2020-08-19 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='recipe_commented',
        ),
    ]
