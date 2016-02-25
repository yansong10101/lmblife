# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type', models.CharField(blank=True, max_length=255)),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('message', models.TextField(blank=True)),
                ('admin', models.ManyToManyField(null=True, to='core.OrgAdmin', related_name='org_admin_message')),
                ('customer', models.ManyToManyField(null=True, to='core.Customer', related_name='customer_message')),
            ],
        ),
        migrations.RenameField(
            model_name='customerupg',
            old_name='approval_comment',
            new_name='admin_comment',
        ),
        migrations.AddField(
            model_name='customerupg',
            name='apply_from_feature',
            field=models.ForeignKey(to='core.Feature', related_name='customer_upg_feature', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customerupg',
            name='customer_comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='customerupg',
            name='is_approve',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='customerupg',
            name='permission_group',
            field=models.ForeignKey(to='core.PermissionGroup', related_name='customer_upg_permission_group', null=True,
                                    blank=True),
        ),
    ]
