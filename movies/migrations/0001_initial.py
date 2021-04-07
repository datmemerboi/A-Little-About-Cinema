# Generated by Django 3.1.2 on 2021-04-07 11:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.CharField(max_length=210, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('director', models.CharField(max_length=100)),
                ('year', models.PositiveIntegerField()),
                ('language', models.CharField(max_length=15)),
                ('short_title', models.CharField(default=None, max_length=50, null=True)),
                ('cast', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, null=True, size=None)),
                ('poster_url', models.TextField(default=None, null=True)),
                ('status', models.SmallIntegerField(default=0)),
                ('why_watch_it', models.TextField(null=True)),
                ('keywords', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=list, size=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
