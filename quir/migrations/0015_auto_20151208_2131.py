# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0014_talk_venue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='talk',
            old_name='speaker',
            new_name='talker',
        ),
    ]
