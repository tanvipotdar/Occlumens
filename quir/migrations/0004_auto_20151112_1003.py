# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0003_auto_20151112_0809'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='no_of_talks',
            new_name='no_of_past_talks',
        ),
        migrations.AddField(
            model_name='venue',
            name='no_of_upcoming_talks',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
