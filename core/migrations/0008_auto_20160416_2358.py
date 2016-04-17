# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160328_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerupg',
            name='apply_level',
            field=models.IntegerField(blank=True, verbose_name='apply user level', default=0),
        ),
        migrations.AlterField(
            model_name='customerupg',
            name='grant_level',
            field=models.IntegerField(blank=True, verbose_name='grant user level', default=0),
        ),
    ]
