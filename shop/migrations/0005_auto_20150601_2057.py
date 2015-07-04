# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20150601_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c')),
                ('order', models.IntegerField(default=0, null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438', blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True, verbose_name='\u0427\u041f\u0423')),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('keywords', models.CharField(max_length=255, null=True, verbose_name='\u041a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0441\u043b\u043e\u0432\u0430', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='item',
            name='manufacturer',
            field=models.ForeignKey(verbose_name='\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c', to='shop.Manufacturer'),
        ),
    ]
