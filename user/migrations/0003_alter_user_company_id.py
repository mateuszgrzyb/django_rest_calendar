# Generated by Django 3.2.2 on 2021-05-11 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_company_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company_id',
            field=models.UUIDField(),
        ),
    ]