# Generated by Django 4.2 on 2023-05-29 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cell_City', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Accessory',
        ),
        migrations.DeleteModel(
            name='AccessoryCategory',
        ),
    ]
