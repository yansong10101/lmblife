# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160324_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='slug_name',
            field=models.SlugField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='feature',
            name='view_type',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
