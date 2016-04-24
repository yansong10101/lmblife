# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160424_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='handle',
            field=models.CharField(unique=True, default='stanford university', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='university',
            name='slug_name',
            field=models.SlugField(unique=True, max_length=255),
        ),
    ]
