# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0021_auto_20151225_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='cache',
            field=models.CharField(default=[], max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='speaker',
            name='cache',
            field=models.CharField(default=[], max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talk',
            name='cache',
            field=models.CharField(default=[], max_length=500),
            preserve_default=False,
        ),
    ]
