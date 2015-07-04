# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to=b'images/%Y/%m', verbose_name='\u0424\u043e\u0442\u043e \u0442\u043e\u0432\u0430\u0440\u0430'),
        ),
    ]
