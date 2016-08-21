# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0010_auto_20151129_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='talks',
            field=models.CharField(default=[], max_length=400),
            preserve_default=False,
        ),
    ]
