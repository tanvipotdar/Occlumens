# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0022_auto_20151225_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='edge_weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='edges',
            field=models.CharField(default=[], max_length=500),
            preserve_default=False,
        ),
    ]
