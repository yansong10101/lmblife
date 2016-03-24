# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160220_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermessage',
            name='created_date',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AddField(
            model_name='customermessage',
            name='last_modified_date',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AddField(
            model_name='customerupg',
            name='apply_level',
            field=models.IntegerField(verbose_name='apply user level', default=0),
        ),
        migrations.AddField(
            model_name='customerupg',
            name='created_date',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AddField(
            model_name='customerupg',
            name='last_modified_date',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
    ]
