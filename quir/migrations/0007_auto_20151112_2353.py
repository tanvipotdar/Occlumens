# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0006_auto_20151112_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='no_of_past_talks',
            new_name='past',
        ),
        migrations.RenameField(
            model_name='list',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='list',
            old_name='no_of_upcoming_talks',
            new_name='upcoming',
        ),
    ]
