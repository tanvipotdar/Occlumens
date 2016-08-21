# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0013_talk_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='venue',
            field=models.ForeignKey(blank=True, to='quir.Venue', null=True),
            preserve_default=True,
        ),
    ]
