# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0015_auto_20151208_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='speaker',
            field=models.ForeignKey(blank=True, to='quir.Speaker', null=True),
            preserve_default=True,
        ),
    ]
