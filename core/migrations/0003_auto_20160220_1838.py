# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160220_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customermessage',
            name='admin',
            field=models.ManyToManyField(related_name='org_admin_message', to='core.OrgAdmin'),
        ),
        migrations.AlterField(
            model_name='customermessage',
            name='customer',
            field=models.ManyToManyField(related_name='customer_message', to='core.Customer'),
        ),
    ]
