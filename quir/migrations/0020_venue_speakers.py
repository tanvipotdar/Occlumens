# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0019_venue_cache'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='speakers',
            field=models.ManyToManyField(to='quir.Speaker', null=True, blank=True),
            preserve_default=True,
        ),
    ]
