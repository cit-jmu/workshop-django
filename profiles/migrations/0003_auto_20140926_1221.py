# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20140925_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='employee_id',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
