# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20160328_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='permissiongroup',
            name='display_name',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
