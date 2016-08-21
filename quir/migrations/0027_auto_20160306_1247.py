# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0026_auto_20160128_0947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='date',
            new_name='name',
        ),
        migrations.AddField(
            model_name='list',
            name='rec',
            field=models.CharField(max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='rec',
            field=models.CharField(max_length=1000, blank=True),
            preserve_default=True,
        ),
    ]
