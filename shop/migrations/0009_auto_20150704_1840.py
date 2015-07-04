# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20150614_1657'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0430 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c', 'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u044b \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u0438'},
        ),
        migrations.AlterField(
            model_name='images',
            name='item',
            field=models.ForeignKey(related_name='images', to='shop.Item'),
        ),
    ]
