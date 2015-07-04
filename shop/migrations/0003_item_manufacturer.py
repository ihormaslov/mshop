# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20150531_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='manufacturer',
            field=models.IntegerField(default=1, choices=[(1, '\u0410\u043d\u0433\u043b\u0438\u044f'), (2, '\u0413\u0435\u0440\u043c\u0430\u043d\u0438\u044f'), (3, '\u0421\u0428\u0410'), (4, '\u0410\u0432\u0441\u0442\u0440\u0438\u044f'), (5, '\u0424\u0440\u0430\u043d\u0446\u0438\u044f'), (6, '\u041d\u0438\u0434\u0435\u0440\u043b\u0430\u043d\u0434\u044b'), (7, '\u0418\u0442\u0430\u043b\u0438\u044f'), (8, '\u0428\u0432\u0435\u0439\u0446\u0430\u0440\u0438\u044f'), (9, '\u0427\u0435\u0445\u0438\u044f'), (10, '\u0425\u043e\u0440\u0432\u0430\u0442\u0438\u044f'), (11, '\u0413\u0440\u0435\u0446\u0438\u044f'), (12, '\u041f\u043e\u043b\u044c\u0448\u0430')]),
            preserve_default=False,
        ),
    ]
