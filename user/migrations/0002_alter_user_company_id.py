# Generated by Django 3.2.2 on 2021-05-11 08:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
