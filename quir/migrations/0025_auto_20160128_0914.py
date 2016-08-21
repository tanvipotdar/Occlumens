# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quir', '0024_auto_20151225_2054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('nodes', models.CharField(max_length=400)),
                ('edges', models.CharField(max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='list',
            name='edge_weight',
        ),
        migrations.RemoveField(
            model_name='speaker',
            name='edge_weight',
        ),
        migrations.RemoveField(
            model_name='talk',
            name='edge_weight',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='edge_weight',
        ),
    ]
