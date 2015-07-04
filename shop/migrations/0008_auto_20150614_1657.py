# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_shopsettings'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShopSettings',
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['order', 'name'], 'verbose_name': '\u0422\u043e\u0432\u0430\u0440', 'verbose_name_plural': '\u0422\u043e\u0432\u0430\u0440\u044b'},
        ),
    ]
