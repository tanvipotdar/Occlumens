# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0016_talk_speaker'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='listos',
            field=models.ManyToManyField(to='quir.List'),
            preserve_default=True,
        ),
    ]
