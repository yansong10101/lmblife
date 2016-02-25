# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, verbose_name='email address', max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('last_login_date', models.DateTimeField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False, editable=False)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('student_id', models.CharField(blank=True, max_length=50)),
                ('offer_number', models.CharField(blank=True, max_length=255)),
                ('photo_url', models.CharField(blank=True, max_length=150)),
                ('is_approved', models.BooleanField(default=False)),
                ('approval_level', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerUPG',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('grant_level', models.IntegerField(verbose_name='grant user level', default=0)),
                ('approval_comment', models.TextField(blank=True)),
                ('customer', models.ForeignKey(to='core.Customer', related_name='customer_upg_customer')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('feature_name', models.CharField(unique=True, max_length=150)),
                ('display_name', models.CharField(blank=True, max_length=150)),
                ('description_wiki_key', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureGroup',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('feature_name', models.CharField(unique=True, max_length=150)),
                ('display_name', models.CharField(blank=True, max_length=150)),
                ('description_wiki_key', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrgAdmin',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], max_length=50, verbose_name='username', error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('email', models.EmailField(verbose_name='email address', max_length=255)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('last_login_date', models.DateTimeField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_president', models.BooleanField(default=False, editable=False)),
                ('is_admin', models.BooleanField(default=False, editable=False)),
                ('prior_level', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('permission_name', models.CharField(max_length=255)),
                ('permission_type', models.CharField(default='r', max_length=2, choices=[('r', 'read only'), ('f', 'full access')])),
                ('is_active', models.BooleanField(default=True)),
                ('feature', models.ForeignKey(to='core.Feature', related_name='feature_permission')),
            ],
        ),
        migrations.CreateModel(
            name='PermissionGroup',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=150)),
                ('is_org_admin', models.BooleanField(default=True)),
                ('is_super_user', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('user_level', models.IntegerField(default=0, choices=[(0, '游客'), (1, '在校生'), (2, '临校生'), (3, '毕业生'), (4, '赞助商'), (5, '黑名单')])),
                ('permission', models.ManyToManyField(related_name='group_permission', to='core.Permission')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('university_name', models.CharField(max_length=255)),
                ('university_code', models.CharField(max_length=50)),
                ('short_name', models.CharField(blank=True, max_length=50)),
                ('display_name', models.CharField(blank=True, max_length=255)),
                ('address_1', models.CharField(blank=True, max_length=255)),
                ('address_2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=50)),
                ('zip_code', models.CharField(blank=True, max_length=10)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('support_email', models.EmailField(blank=True, max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=20)),
                ('official_website', models.URLField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='orgadmin',
            name='permission_group',
            field=models.ManyToManyField(related_name='org_permission_group', to='core.PermissionGroup'),
        ),
        migrations.AddField(
            model_name='orgadmin',
            name='university',
            field=models.ForeignKey(to='core.University', related_name='org_admin_university'),
        ),
        migrations.AddField(
            model_name='feature',
            name='feature_group',
            field=models.ForeignKey(to='core.FeatureGroup', related_name='feature_group'),
        ),
        migrations.AddField(
            model_name='customerupg',
            name='permission_group',
            field=models.ForeignKey(to='core.PermissionGroup', related_name='customer_upg_permission_group', null=True),
        ),
        migrations.AddField(
            model_name='customerupg',
            name='university',
            field=models.ForeignKey(to='core.University', related_name='customer_upg_university'),
        ),
    ]
