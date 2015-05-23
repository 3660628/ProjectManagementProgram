# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0003_auto_20150401_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='date_created',
            field=models.DateField(default=datetime.date(2015, 5, 9)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genericbase',
            name='date_created',
            field=models.DateField(default=datetime.date(2015, 5, 9)),
            preserve_default=True,
        ),
    ]
