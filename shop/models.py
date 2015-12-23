# coding: utf-8
from datetime import datetime
import decimal

from django.db import models
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField

from project.settings import CURRENCY_USD

from shop import const


class Division(models.Model):
    order = models.IntegerField(verbose_name=u'Порядок сортировки', blank=True, null=True, default=0)
    parent = models.ForeignKey('self', verbose_name=u'Родительсткая категория', related_name='children', blank=True, null=True)
    publicated = models.BooleanField(verbose_name=u'Опубликовано', default=True)
    count = models.IntegerField(blank=True, null=True)

    date = models.DateTimeField(default=datetime.now, verbose_name=u'Дата добавления')
    modified = models.DateTimeField(auto_now=True)

    # seo
    slug = models.SlugField(verbose_name=u'ЧПУ', unique=True)
    description = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    keywords = models.CharField(verbose_name=u'Ключевые слова', max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Category(Division):
    name = models.CharField(max_length=255, verbose_name=u'Название категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug or self.id})

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class Manufacturer(Division):
    name = models.CharField(max_length=100, verbose_name=u'Производитель')

    def get_absolute_url(self):
        return reverse('manufacturer', kwargs={'slug': self.slug or self.id})

    class Meta:
        verbose_name = u'Страна производитель'
        verbose_name_plural = u'Страны производители'


class Item(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'Категория', related_name='c_items')
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=u'Производитель', related_name='m_items')

    name = models.CharField(max_length=255, verbose_name=u'Название товара')
    order = models.IntegerField(verbose_name=u'Порядок сортировки', blank=True, null=True, default=0)
    publicated = models.BooleanField(verbose_name=u'Опубликовано', default=True)
    in_store = models.BooleanField(verbose_name=u'В наличии', default=True)
    item_description = RichTextField(verbose_name=u'Описание товара', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=u'Цена')
    date = models.DateTimeField(default=datetime.now, verbose_name=u'Дата добавления')
    modified = models.DateTimeField(auto_now=True)

    # seo
    slug = models.SlugField(verbose_name=u'ЧПУ', unique=True)
    description = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    keywords = models.CharField(verbose_name=u'Ключевые слова', max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item', kwargs={
            'category_slug': self.category.slug or self.category.id,
            'self_slug': self.slug or self.id
        })

    def price_currency(self):
        return self.price * CURRENCY_USD

    def is_new(self):
        """
        Calculate delta from time when item was added and now.
        """
        pass


class Images(models.Model):
    item = models.ForeignKey(Item, related_name='images')
    image = models.ImageField(upload_to='images/%Y/%m', verbose_name=u'Фото товара')

    class Meta:
        verbose_name = u'Фото'
        verbose_name_plural = u'Фото'


class Properties(models.Model):
    """
    Свойства товаров
    """
    propName = models.CharField(max_length=100, verbose_name=u'Свойство', blank=True)
    order = models.IntegerField(verbose_name=u'Порядок сортировки', blank=True, null=True, default=0)
    category = models.ForeignKey(Category, verbose_name=u'Привязка к категории', blank=True, null=True)

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


class CartItems(models.Model):
    """
    Корзина товаров
    """
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Item, unique=False)

    class Meta:
        ordering = ['date_added']

    def total(self):
        return int(self.quantity) * int(self.product.price_currency())

    def cart_total(self):
        cart_total = decimal.Decimal('0.00')
        for i in CartItems.objects.filter(cart_id=self.cart_id):
            cart_total += i.total()
        return cart_total

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save()


class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=u'Имя')
    last_name = models.CharField(max_length=50, verbose_name=u'Фамилия')
    phone = models.CharField(max_length=20, verbose_name=u'Телефон')
    email = models.EmailField(max_length=50, verbose_name=u'E-mail', blank=True, null=True)

    ship_method = models.IntegerField(choices=const.SHIP_METHOD, default=1, verbose_name=u'Способ доставки')
    comment = models.TextField(max_length=3000, verbose_name=u'Комментарий к заказу', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата')
    status = models.IntegerField(choices=const.ORDER_STATUS, default=1, verbose_name=u'Статус заказа')
    last_updated = models.DateTimeField(auto_now=True, verbose_name=u'Последнее обновление')

    def __unicode__(self):
        return u'Заказ № %s' % str(self.id)

    def total(self):
        total = decimal.Decimal('0.00')
        for item in OrderedItems.objects.filter(order=self):
            total += item.total()
        return total

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'


class OrderedItems(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Item)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'

    def __unicode__(self):
        return self.product.name

    def total(self):
        return self.quantity * self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()


class HomeSlider(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Название слайда')
    image = models.ImageField(upload_to='images/%Y/%m', verbose_name=u'Картинка слайдера')
    link = models.URLField(max_length=200, verbose_name=u'Ссылка')
    text = RichTextField(max_length=500, verbose_name=u'Текст слайда')

    class Meta:
        verbose_name = u'Слайдер на главной'
        verbose_name_plural = u'Слайдеры на главной'
