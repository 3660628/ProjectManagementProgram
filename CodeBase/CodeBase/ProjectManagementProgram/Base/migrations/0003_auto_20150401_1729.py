# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0002_auto_20150315_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='date_created',
            field=models.DateField(default=datetime.date(2015, 4, 1)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genericbase',
            name='date_created',
            field=models.DateField(default=datetime.date(2015, 4, 1)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genericbase',
            name='user_creator',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
