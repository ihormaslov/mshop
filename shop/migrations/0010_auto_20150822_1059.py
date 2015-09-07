# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20150704_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='call_time',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ip_address',
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(default=datetime.datetime(2015, 8, 22, 10, 59, 12, 732063, tzinfo=utc), max_length=50, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(related_name='items', verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', to='shop.Category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='manufacturer',
            field=models.ForeignKey(related_name='items', verbose_name='\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c', to='shop.Manufacturer'),
        ),
        migrations.RemoveField(
            model_name='properties',
            name='category',
        ),
        migrations.AddField(
            model_name='properties',
            name='category',
            field=models.ForeignKey(verbose_name='\u041f\u0440\u0438\u0432\u044f\u0437\u043a\u0430 \u043a \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438', blank=True, to='shop.Category', null=True),
        ),
    ]
