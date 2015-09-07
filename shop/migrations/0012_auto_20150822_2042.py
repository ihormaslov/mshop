# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20150822_2009'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homeslider',
            options={'verbose_name': '\u0421\u043b\u0430\u0439\u0434\u0435\u0440 \u043d\u0430 \u0433\u043b\u0430\u0432\u043d\u043e\u0439', 'verbose_name_plural': '\u0421\u043b\u0430\u0439\u0434\u0435\u0440\u044b \u043d\u0430 \u0433\u043b\u0430\u0432\u043d\u043e\u0439'},
        ),
        migrations.AlterField(
            model_name='homeslider',
            name='text',
            field=ckeditor.fields.RichTextField(max_length=500, verbose_name='\u0422\u0435\u043a\u0441\u0442 \u0441\u043b\u0430\u0439\u0434\u0430'),
        ),
    ]
