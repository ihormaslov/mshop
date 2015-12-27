# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20150822_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='parent',
            field=models.ForeignKey(related_name='children', verbose_name='\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u043a\u0430\u044f \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', blank=True, to='shop.Manufacturer', null=True),
        ),
    ]
