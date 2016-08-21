# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0011_list_talks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talk',
            name='venue',
        ),
    ]
