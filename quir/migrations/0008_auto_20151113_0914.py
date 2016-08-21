# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0007_auto_20151112_2353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='speaker',
            old_name='name',
            new_name='title',
        ),
    ]
