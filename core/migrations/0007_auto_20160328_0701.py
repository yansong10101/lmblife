# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160328_0613'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerupg',
            old_name='is_approve',
            new_name='is_approved',
        ),
        migrations.AddField(
            model_name='permissiongroup',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='permissiongroup',
            name='slug_name',
            field=models.SlugField(max_length=250, blank=True),
        ),
        migrations.AddField(
            model_name='university',
            name='slug_name',
            field=models.SlugField(max_length=300, blank=True),
        ),
    ]
