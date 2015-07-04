# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import ckeditor.fields
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cart_id', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['date_added'],
                'db_table': 'cart_items',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438')),
                ('order', models.IntegerField(default=0, null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438', blank=True)),
                ('publicated', models.BooleanField(default=True, verbose_name='\u041e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d\u043e')),
                ('slug', models.SlugField(null=True, verbose_name='\u0427\u041f\u0423', blank=True)),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('keywords', models.CharField(max_length=255, null=True, verbose_name='\u041a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0441\u043b\u043e\u0432\u0430', blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(related_name='children', verbose_name='\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u043a\u0430\u044f \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', blank=True, to='shop.Category', null=True)),
            ],
            options={
                'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f',
                'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'images/%Y/%m', verbose_name='\u0424\u043e\u0442\u043e \u0442\u043e\u0432\u0430\u0440\u0430')),
            ],
            options={
                'verbose_name': '\u0424\u043e\u0442\u043e',
                'verbose_name_plural': '\u0424\u043e\u0442\u043e',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430')),
                ('order', models.IntegerField(default=0, null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438', blank=True)),
                ('publicated', models.BooleanField(default=True, verbose_name='\u041e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d\u043e')),
                ('inStore', models.BooleanField(default=True, verbose_name='\u0412 \u043d\u0430\u043b\u0438\u0447\u0438\u0438')),
                ('item_description', ckeditor.fields.RichTextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430', blank=True)),
                ('price', models.DecimalField(verbose_name='\u0426\u0435\u043d\u0430', max_digits=10, decimal_places=0)),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(null=True, blank=True, unique=True, verbose_name='\u0427\u041f\u0423')),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('keywords', models.CharField(max_length=255, null=True, verbose_name='\u041a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0441\u043b\u043e\u0432\u0430', blank=True)),
                ('category', models.ForeignKey(verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', to='shop.Category')),
            ],
            options={
                'verbose_name': '\u0422\u043e\u0432\u0430\u0440',
                'verbose_name_plural': '\u0422\u043e\u0432\u0430\u0440\u044b',
            },
        ),
        migrations.CreateModel(
            name='ItemProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('propValue', models.CharField(max_length=100, null=True, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435', blank=True)),
                ('item', models.ForeignKey(to='shop.Item')),
            ],
            options={
                'verbose_name': '\u0421\u0432\u043e\u0439\u0441\u0442\u0432\u043e',
                'verbose_name_plural': '\u0421\u0432\u043e\u0439\u0441\u0442\u0432\u0430',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50, verbose_name='\u0418\u043c\u044f')),
                ('phone', models.CharField(max_length=20, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('email', models.EmailField(max_length=50, null=True, verbose_name='E-mail', blank=True)),
                ('call_time', models.CharField(max_length=50, null=True, verbose_name='\u0423\u0434\u043e\u0431\u043d\u043e\u0435 \u0432\u0440\u0435\u043c\u044f \u0434\u043b\u044f \u0437\u0432\u043e\u043d\u043a\u0430', blank=True)),
                ('ship_method', models.IntegerField(verbose_name='\u0421\u043f\u043e\u0441\u043e\u0431 \u0434\u043e\u0441\u0442\u0430\u0432\u043a\u0438', choices=[(1, b'\xd0\x9d\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x8f \xd0\xbf\xd0\xbe\xd1\x87\xd1\x82\xd0\xb0'), (2, b'\xd0\x90\xd0\xb2\xd1\x82\xd0\xbe\xd0\xbb\xd1\x8e\xd0\xba\xd1\x81'), (3, b'\xd0\x93\xd1\x8e\xd0\xbd\xd1\x81\xd0\xb5\xd0\xbb'), (4, b'\xd0\x9c\xd1\x96\xd1\x81\xd1\x82 \xd0\x95\xd0\xba\xd1\x81\xd0\xbf\xd1\x80\xd0\xb5\xd1\x81')])),
                ('comment', models.TextField(max_length=3000, null=True, verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043a \u0437\u0430\u043a\u0430\u0437\u0443', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430')),
                ('status', models.IntegerField(default=1, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u043a\u0430\u0437\u0430', choices=[(1, b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xbd\xd1\x8f\xd1\x82\xd0\xbe'), (2, b'\xd0\x9e\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xb0\xd0\xbd\xd0\xbd\xd0\xbe'), (3, b'\xd0\x94\xd0\xbe\xd1\x81\xd1\x82\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xbe'), (4, b'\xd0\x9e\xd1\x82\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xbe')])),
                ('ip_address', models.IPAddressField(null=True, verbose_name='ip-\u0430\u0434\u0440\u0435\u0441 \u0437\u0430\u043a\u0430\u0437\u0447\u0438\u043a\u0430', blank=True)),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0435 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u043a\u0430\u0437',
                'verbose_name_plural': '\u0417\u0430\u043a\u0430\u0437\u044b',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('order', models.ForeignKey(to='shop.Order')),
                ('product', models.ForeignKey(to='shop.Item')),
            ],
            options={
                'verbose_name': '\u0422\u043e\u0432\u0430\u0440',
                'verbose_name_plural': '\u0422\u043e\u0432\u0430\u0440\u044b',
            },
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('propName', models.CharField(max_length=100, verbose_name='\u0421\u0432\u043e\u0439\u0441\u0442\u0432\u043e', blank=True)),
                ('order', models.IntegerField(default=0, null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438', blank=True)),
                ('category', models.ManyToManyField(to='shop.Category', null=True, verbose_name='\u041f\u0440\u0438\u0432\u044f\u0437\u043a\u0430 \u043a \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438', blank=True)),
            ],
            options={
                'verbose_name': '\u0421\u0432\u043e\u0439\u0441\u0442\u0432\u043e',
                'verbose_name_plural': '\u0421\u0432\u043e\u0439\u0441\u0442\u0432\u0430',
            },
        ),
        migrations.AddField(
            model_name='itemproperties',
            name='prop',
            field=models.ForeignKey(verbose_name='\u0421\u0432\u043e\u0439\u0441\u0442\u0432\u043e', blank=True, to='shop.Properties', null=True),
        ),
        migrations.AddField(
            model_name='images',
            name='item',
            field=models.ForeignKey(to='shop.Item'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(to='shop.Item'),
        ),
    ]
