# Generated by Django 3.2.2 on 2021-05-11 09:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 9, 46, 29, 447092)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 9, 46, 29, 447080)),
        ),
    ]