# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0018_venue_lists'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='cache',
            field=models.CharField(default=[], max_length=200),
            preserve_default=False,
        ),
    ]
