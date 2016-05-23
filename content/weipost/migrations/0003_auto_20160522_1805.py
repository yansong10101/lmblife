# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20160515_0136'),
        ('weipost', '0002_jiejipost_post_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jiejicomment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='jiejipost',
            name='feature',
        ),
        migrations.RemoveField(
            model_name='jiejipost',
            name='user',
        ),
        migrations.AddField(
            model_name='jiejicomment',
            name='author',
            field=models.ForeignKey(null=True, to='core.Customer', related_name='wei_comment_author'),
        ),
        migrations.AddField(
            model_name='jiejicomment',
            name='mentioned',
            field=models.ManyToManyField(to='core.Customer', related_name='wei_comment_mentioned'),
        ),
        migrations.AddField(
            model_name='jiejipost',
            name='author',
            field=models.ForeignKey(null=True, to='core.Customer', related_name='wei_post_author'),
        ),
        migrations.AddField(
            model_name='jiejipost',
            name='mentioned',
            field=models.ManyToManyField(to='core.Customer', related_name='wei_port_mentioned'),
        ),
        migrations.AlterField(
            model_name='jiejicomment',
            name='admin',
            field=models.ForeignKey(null=True, to='core.OrgAdmin', related_name='wei_comment_admin'),
        ),
        migrations.AlterField(
            model_name='jiejipost',
            name='admin',
            field=models.ForeignKey(null=True, to='core.OrgAdmin', related_name='wei_post_admin'),
        ),
    ]
