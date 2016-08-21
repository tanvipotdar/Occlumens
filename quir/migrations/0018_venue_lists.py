# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0017_talk_listos'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='lists',
            field=models.ManyToManyField(to='quir.List'),
            preserve_default=True,
        ),
    ]
