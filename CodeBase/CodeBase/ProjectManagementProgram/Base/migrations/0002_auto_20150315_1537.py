# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='link',
            new_name='link_text',
        ),
    ]
