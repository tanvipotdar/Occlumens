# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0008_auto_20151113_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='abstract',
            field=models.TextField(default='Abstract not available'),
            preserve_default=False,
        ),
    ]
