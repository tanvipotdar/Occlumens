# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0005_auto_20151112_1014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='name',
            new_name='title',
        ),
    ]
