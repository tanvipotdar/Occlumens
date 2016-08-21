# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0020_venue_speakers'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='lists',
            field=models.ManyToManyField(to='quir.List'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='venue',
            name='cache',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
    ]
