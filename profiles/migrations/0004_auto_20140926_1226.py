# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20140926_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='employee_id',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
