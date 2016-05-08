# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20160424_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='avatar_url',
            field=models.CharField(max_length=225, blank=True),
        ),
    ]
