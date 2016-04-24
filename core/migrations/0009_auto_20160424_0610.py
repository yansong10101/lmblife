# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20160416_2358'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniversityAdditionalAttributes',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('attribute_name', models.CharField(max_length=255)),
                ('attribute_value', models.CharField(max_length=255, blank=True)),
                ('attribute_long_value', models.TextField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='university',
            name='short_name',
        ),
        migrations.RemoveField(
            model_name='university',
            name='university_name',
        ),
        migrations.AddField(
            model_name='university',
            name='handle',
            field=models.CharField(max_length=255, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='university',
            name='display_name',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='university',
            name='slug_name',
            field=models.SlugField(max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='universityadditionalattributes',
            name='university',
            field=models.ForeignKey(related_name='university', to='core.University'),
        ),
    ]
