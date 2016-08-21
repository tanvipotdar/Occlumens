# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0023_auto_20151225_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='edge_weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='list',
            name='edges',
            field=models.CharField(default=[], max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='speaker',
            name='edge_weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='speaker',
            name='edges',
            field=models.CharField(default=[], max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talk',
            name='edge_weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talk',
            name='edges',
            field=models.CharField(default=[], max_length=500),
            preserve_default=False,
        ),
    ]
