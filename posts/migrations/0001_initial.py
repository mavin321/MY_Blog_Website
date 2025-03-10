# Generated by Django 5.1 on 2025-02-25 23:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=40)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('image', models.CharField(max_length=50)),
            ],
        ),
    ]
