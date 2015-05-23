# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alert', models.TextField()),
                ('date_created', models.DateField(default=datetime.date(2015, 3, 15))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenericBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateField(default=datetime.date(2015, 3, 15))),
                ('last_modified', models.DateField(null=True, blank=True)),
                ('date_closed', models.DateField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('genericbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Base.GenericBase')),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField(null=True, blank=True)),
                ('file', models.FileField(upload_to=b'')),
            ],
            options={
            },
            bases=('Base.genericbase',),
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('genericbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Base.GenericBase')),
                ('title', models.CharField(max_length=60, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('conclusion', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=('Base.genericbase',),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('genericbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Base.GenericBase')),
                ('comment', models.TextField()),
            ],
            options={
            },
            bases=('Base.genericbase',),
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('genericbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Base.GenericBase')),
                ('post', models.TextField()),
            ],
            options={
            },
            bases=('Base.genericbase',),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('genericbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Base.GenericBase')),
                ('title', models.CharField(max_length=60, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=('Base.genericbase',),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('genericbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Base.GenericBase')),
                ('title', models.TextField()),
                ('link', models.TextField()),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=('Base.genericbase',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60, null=True, blank=True)),
                ('homepage_text', models.TextField(null=True, blank=True)),
                ('conclusion', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=60, null=True, blank=True)),
                ('department', models.CharField(max_length=60, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_creator', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('project', models.ForeignKey(to='Base.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='link',
            name='project',
            field=models.ForeignKey(to='Base.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericbase',
            name='user_closed',
            field=models.ForeignKey(related_name='user_closed', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericbase',
            name='user_creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericbase',
            name='user_last_modified',
            field=models.ForeignKey(related_name='user_last_modified', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='project',
            field=models.ForeignKey(to='Base.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discussion',
            name='project',
            field=models.ForeignKey(to='Base.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='discussion',
            field=models.ForeignKey(to='Base.Discussion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(to='Base.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='blog',
            field=models.ForeignKey(to='Base.Blog'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='parent_entry',
            field=models.ForeignKey(blank=True, to='Base.BlogPost', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blog',
            name='project',
            field=models.ForeignKey(to='Base.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='project',
            field=models.ForeignKey(to='Base.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='user_creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
