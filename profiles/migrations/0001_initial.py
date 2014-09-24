# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('employee_id', models.PositiveIntegerField()),
                ('phone_number', models.CharField(max_length=25, editable=False)),
                ('mailbox', models.CharField(max_length=25, editable=False)),
                ('department', models.CharField(max_length=255, editable=False)),
                ('affiliation', models.CharField(max_length=25, editable=False)),
                ('nickname', models.CharField(max_length=25, editable=False, blank=True)),
                ('computer_preference', models.CharField(default=b'pc', max_length=6, choices=[(b'mac', b'Mac'), (b'pc', b'PC')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
