# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-18 22:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('last_login_date', models.DateTimeField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=16)),
                ('address_1', models.CharField(blank=True, max_length=225)),
                ('address_2', models.CharField(blank=True, max_length=225)),
                ('city', models.CharField(blank=True, max_length=150)),
                ('state', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(blank=True, max_length=50)),
                ('zip', models.CharField(blank=True, max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('avatar_url', models.CharField(blank=True, max_length=225)),
            ],
            options={
                'db_table': 'lmb_model_customer',
            },
        ),
    ]
