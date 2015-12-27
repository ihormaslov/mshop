# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20151018_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='count',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
