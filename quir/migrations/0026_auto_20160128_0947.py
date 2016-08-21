# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0025_auto_20160128_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.CharField(default=b'', max_length=400),
            preserve_default=True,
        ),
    ]
