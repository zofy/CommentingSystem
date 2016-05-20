# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-17 19:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='children',
        ),
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 5, 17, 19, 3, 23, 648000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='depth',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='path',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]