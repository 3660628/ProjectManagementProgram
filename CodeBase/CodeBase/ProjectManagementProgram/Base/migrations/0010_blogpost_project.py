# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0009_auto_20150509_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='project',
            field=models.ForeignKey(default=1, to='Base.Project'),
            preserve_default=False,
        ),
    ]
