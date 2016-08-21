# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0009_talk_abstract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='lists',
            field=models.CharField(max_length=400),
            preserve_default=True,
        ),
    ]
