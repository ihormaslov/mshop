# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'shop_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['shop.Category'])),
            ('publicated', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Category'])

        # Adding model 'Properties'
        db.create_table(u'shop_properties', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('propName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Category'])),
        ))
        db.send_create_signal(u'shop', ['Properties'])

        # Adding model 'Item'
        db.create_table(u'shop_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('publicated', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('inStore', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('item_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.CharField')(default=0, max_length=10)),
            ('action_item', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('add_in_slider', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Item'])

        # Adding model 'ItemProperties'
        db.create_table(u'shop_itemproperties', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Item'])),
            ('prop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Properties'], null=True, blank=True)),
            ('propValue', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['ItemProperties'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'shop_category')

        # Deleting model 'Properties'
        db.delete_table(u'shop_properties')

        # Deleting model 'Item'
        db.delete_table(u'shop_item')

        # Deleting model 'ItemProperties'
        db.delete_table(u'shop_itemproperties')


    models = {
        u'shop.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['shop.Category']"}),
            'publicated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'shop.item': {
            'Meta': {'object_name': 'Item'},
            'action_item': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'add_in_slider': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Category']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'inStore': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'item_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'publicated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'shop.itemproperties': {
            'Meta': {'object_name': 'ItemProperties'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Item']"}),
            'prop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Properties']", 'null': 'True', 'blank': 'True'}),
            'propValue': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'shop.properties': {
            'Meta': {'object_name': 'Properties'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'propName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['shop']