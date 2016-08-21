# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0012_remove_talk_venue'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='place',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
