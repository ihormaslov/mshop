# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_manufacturer_publicated'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('currency', models.DecimalField(verbose_name='\u041a\u0443\u0440\u0441 \u0432\u0430\u043b\u044e\u0442\u044b', max_digits=6, decimal_places=2)),
            ],
        ),
    ]
