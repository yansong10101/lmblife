# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-19 23:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('display_name', models.CharField(blank=True, max_length=500)),
                ('alternative_name', models.CharField(blank=True, max_length=500)),
                ('university_code', models.CharField(max_length=50)),
                ('address_1', models.CharField(blank=True, max_length=255)),
                ('address_2', models.CharField(blank=True, max_length=255)),
                ('district', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=50)),
                ('zip_code', models.CharField(blank=True, max_length=10)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('support_email', models.EmailField(blank=True, max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=20)),
                ('official_website', models.URLField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'lmb_model_university',
            },
        ),
        migrations.CreateModel(
            name='UniversityAdditionalAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_name', models.CharField(max_length=255)),
                ('attribute_value', models.CharField(blank=True, max_length=255)),
                ('attribute_long_value', models.TextField(blank=True)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='university', to='university.University')),
            ],
            options={
                'db_table': 'lmb_model_university_additional_attributes',
            },
        ),
    ]
