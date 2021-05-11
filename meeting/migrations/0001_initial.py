# Generated by Django 3.2.2 on 2021-05-11 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('agenda', models.TextField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('location', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.room')),
            ],
        ),
    ]
