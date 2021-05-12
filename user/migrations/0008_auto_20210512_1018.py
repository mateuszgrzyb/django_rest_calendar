# Generated by Django 3.2.2 on 2021-05-12 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]
