# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0002_auto_20151111_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='speaker',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talk',
            name='venue',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
