# coding: utf-8
from PIL import Image as PIL
from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse


class Category(models.Model):
    """
    Категория товаров
    """
    title = models.CharField(max_length=255, verbose_name=u'Название категории')
    order = models.IntegerField(verbose_name=u'Порядок сортировки', blank=True, null=True, default=0)
    parent = models.ForeignKey('self', verbose_name=u'Родительсткая категория', related_name='children', blank=True, null=True)
    publicated = models.BooleanField(verbose_name=u'Опубликовано', default=True)

    # seo
    slug = models.SlugField(verbose_name=u'ЧПУ', blank=True, null=True)
    description = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    keywords = models.CharField(verbose_name=u'Ключевые слова', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug or self.id})


    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class Item(models.Model):
    """
    Товар в категории
    """
    category = models.ForeignKey(Category)

    title = models.CharField(max_length=255, verbose_name=u'Название товара')
    order = models.IntegerField(verbose_name=u'Порядок сортировки', blank=True, null=True, default=0)
    publicated = models.BooleanField(verbose_name=u'Опубликовано', default=True)
    inStore = models.BooleanField(verbose_name=u'В наличии', default=True)
    image = models.ImageField(upload_to='images/%Y/%m', verbose_name=u'Фото товара')
    date = models.DateTimeField(default=datetime.now, verbose_name=u'Дата добавления')
    item_description = models.TextField(verbose_name=u'Описание товара', blank=True, null=True)
    short_description = models.TextField(verbose_name=u'Краткое описание товара', blank=True, null=True)
    price = models.CharField(max_length=10, verbose_name=u'Цена', default=0)

    action_item = models.BooleanField(default=False, verbose_name='Акция')
    add_in_slider = models.BooleanField(default=False, verbose_name='Добавить в слайдер')

    # seo
    slug = models.SlugField(verbose_name=u'ЧПУ', blank=True, null=True)
    description = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    keywords = models.CharField(verbose_name=u'Ключевые слова', max_length=255, blank=True, null=True)

    def __unicode__(self):
       # return ('%s', '%s', '%s', '%s') % (self.title, self.price, self.item_description, self.image)
        return self.title

    def get_absolute_url(self):
        return reverse('item', kwargs={
            'category_slug': self.category.slug or self.category.id,
            'self_slug': self.slug or self.id
        })

    class Meta:
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'


class Properties(models.Model):
    """
    Свойства товаров
    """
    propName = models.CharField(max_length=100, verbose_name=u'Свойство', blank=True)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.propName

    class Meta:
            verbose_name = u'Свойство'
            verbose_name_plural = u'Свойства'


class ItemProperties(models.Model):
    """
    модель, объеденяющая свойства товаров и сами товары
    """
    item = models.ForeignKey(Item)
    prop = models.ForeignKey(Properties, verbose_name=u'Свойство', blank=True, null=True)
    propValue = models.CharField(max_length=100, verbose_name=u'Значение', blank=True, null=True)

    def __unicode__(self):
        return self.propValue

    class Meta:
            verbose_name = u'Свойство'
            verbose_name_plural = u'Свойства'