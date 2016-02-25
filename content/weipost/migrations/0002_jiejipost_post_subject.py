# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weipost', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jiejipost',
            name='post_subject',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
