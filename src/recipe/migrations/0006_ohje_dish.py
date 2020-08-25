# Generated by Django 3.0.6 on 2020-07-28 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_remove_ohje_dish'),
    ]

    operations = [
        migrations.AddField(
            model_name='ohje',
            name='dish',
            field=models.CharField(choices=[('ALKUPALA', 'Alkupala'), ('PÄÄRUOKA', 'Pääruoka'), ('JÄLKIRUOKA', 'Jälkiruoka'), ('JUOMA', 'Juoma')], default='PÄÄRUOKA', max_length=12),
        ),
    ]