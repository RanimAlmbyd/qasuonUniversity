# Generated by Django 5.0.1 on 2024-03-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_addresstwo_address_one'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buses',
            name='phone',
            field=models.IntegerField(max_length=20),
        ),
    ]
