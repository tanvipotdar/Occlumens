# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0004_auto_20151112_1003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='no_of_past_talks',
            new_name='past',
        ),
        migrations.RenameField(
            model_name='venue',
            old_name='no_of_upcoming_talks',
            new_name='upcoming',
        ),
    ]
