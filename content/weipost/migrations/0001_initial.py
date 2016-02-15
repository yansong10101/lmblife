# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JieJiComment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('comment_message', models.TextField()),
                ('like_count', models.IntegerField(default=0)),
                ('admin', models.ForeignKey(null=True, related_name='jie_ji_comment_admin', to='core.OrgAdmin')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JieJiPost',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('post_message', models.TextField()),
                ('comments_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('admin', models.ForeignKey(null=True, related_name='jie_ji_post_admin', to='core.OrgAdmin')),
                ('feature', models.ForeignKey(related_name='wei_post_feature', to='core.Feature')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('tag_name', models.CharField(max_length=255, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='jiejipost',
            name='post_tag',
            field=models.ManyToManyField(related_name='jie_ji_post_post_tag', to='weipost.PostTag'),
        ),
        migrations.AddField(
            model_name='jiejipost',
            name='university',
            field=models.ForeignKey(related_name='wei_post_university', to='core.University'),
        ),
        migrations.AddField(
            model_name='jiejipost',
            name='user',
            field=models.ForeignKey(null=True, related_name='jie_ji_post_user', to='core.Customer'),
        ),
        migrations.AddField(
            model_name='jiejicomment',
            name='post',
            field=models.ForeignKey(related_name='jie_ji_post', to='weipost.JieJiPost'),
        ),
        migrations.AddField(
            model_name='jiejicomment',
            name='user',
            field=models.ForeignKey(null=True, related_name='jie_ji_comment_user', to='core.Customer'),
        ),
    ]
