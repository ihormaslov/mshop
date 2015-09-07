# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20150822_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeSlider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u043b\u0430\u0439\u0434\u0430')),
                ('text', models.CharField(max_length=500, verbose_name='\u0422\u0435\u043a\u0441\u0442 \u0441\u043b\u0430\u0439\u0434\u0430')),
                ('image', models.ImageField(upload_to=b'images/%Y/%m', verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430 \u0441\u043b\u0430\u0439\u0434\u0435\u0440\u0430')),
                ('link', models.URLField(verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='ship_method',
            field=models.IntegerField(default=1, verbose_name='\u0421\u043f\u043e\u0441\u043e\u0431 \u0434\u043e\u0441\u0442\u0430\u0432\u043a\u0438', choices=[(1, b'\xd0\x9d\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x8f \xd0\xbf\xd0\xbe\xd1\x87\xd1\x82\xd0\xb0'), (2, b'\xd0\x90\xd0\xb2\xd1\x82\xd0\xbe\xd0\xbb\xd1\x8e\xd0\xba\xd1\x81'), (3, b'\xd0\x93\xd1\x8e\xd0\xbd\xd1\x81\xd0\xb5\xd0\xbb'), (4, b'\xd0\x9c\xd1\x96\xd1\x81\xd1\x82 \xd0\x95\xd0\xba\xd1\x81\xd0\xbf\xd1\x80\xd0\xb5\xd1\x81')]),
        ),
    ]
