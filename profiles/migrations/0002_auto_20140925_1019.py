# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='affiliation',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mailbox',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(max_length=25, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=25),
        ),
    ]
