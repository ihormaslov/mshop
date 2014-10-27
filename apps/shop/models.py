# coding: utf-8
from datetime import datetime
import decimal

from django.db import models
from django.core.urlresolvers import reverse
from easy_thumbnails.fields import ThumbnailerImageField


class Category(models.Model):
    """
    Категория товаров
    """
    title = models.CharField(max_length=255, verbose_name=u'Название категории')
    order = models.IntegerField(verbose_name=u'Порядок сортировки', blank=True, null=True, default=0)
    parent = models.ForeignKey('self', verbose_name=u'Родительсткая категория', related_name='children', blank=True, null=True)
    publicated = models.BooleanField(verbose_name=u'Опубликовано', default=True)
    image = ThumbnailerImageField(upload_to='images/categories', verbose_name=u'Картинка категории (960х150)',
                                  blank=True, null=True)

    # seo
    slug = models.SlugField(verbose_name=u'ЧПУ', blank=True, null=True)
    description = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    keywords = models.CharField(verbose_name=u'Ключевые слова', max_length=255, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug or self.id})

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class Manufacturer(models.Model):
    """
    Страны производители товара
    """
    country_name = models.CharField(max_length=255, verbose_name=u'Страна производитель')
    order = models.IntegerField(verbose_name=u'Порядок сортировки', blank=True, null=True, default=0)
    logo = ThumbnailerImageField(upload_to='images/manufacturers', verbose_name=u'Логотип производителя')
    image = ThumbnailerImageField(upload_to='images/manufacturers', verbose_name=u'Большой лого (960х150)', blank=True,
                                  null=True)
    modified = models.DateTimeField(auto_now=True)

    # seo
    slug = models.SlugField(verbose_name=u'ЧПУ', blank=True, null=True, unique=True)
    description = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    keywords = models.CharField(verbose_name=u'Ключевые слова', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.country_name

    def get_absolute_url(self):
        return reverse('manufacturer', kwargs={'slug': self.slug or self.id})

    class Meta:
        verbose_name = u'Производитель'
        verbose_name_plural = u'Производители'


class Item(models.Model):
    """
    Товар в категории
    """
    category = models.ForeignKey(Category, verbose_name=u'Категория')
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=u'Страна производитель')

    title = models.CharField(max_length=255, verbose_name=u'Название товара')
    order = models.IntegerField(verbose_name=u'Порядок сортировки', blank=True, null=True, default=0)
    publicated = models.BooleanField(verbose_name=u'Опубликовано', default=True)
    inStore = models.BooleanField(verbose_name=u'В наличии', default=True)
    image = ThumbnailerImageField(upload_to='images/%Y/%m', verbose_name=u'Фото товара')
    date = models.DateTimeField(default=datetime.now, verbose_name=u'Дата добавления')
    modified = models.DateTimeField(auto_now=True)
    item_description = models.TextField(verbose_name=u'Описание товара', blank=True, null=True)
    price = models.CharField(max_length=10, verbose_name=u'Цена', default=0)
    old_price = models.CharField(max_length=10, verbose_name=u'Старая цена', default=0)

    action_item = models.BooleanField(default=False, verbose_name='Акция')
    # add_in_slider = models.BooleanField(default=False, verbose_name='Добавить в слайдер')

    # seo
    slug = models.SlugField(verbose_name=u'ЧПУ', blank=True, null=True, unique=True)
    description = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    keywords = models.CharField(verbose_name=u'Ключевые слова', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item', kwargs={
            'category_slug': self.category.slug or self.category.id,
            'self_slug': self.slug or self.id
        })

    class Meta:
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'


class AdditionalImages(models.Model):
    """
    Модель дополнительных изображений товара
    """
    item = models.ForeignKey(Item)
    image = ThumbnailerImageField(upload_to='images/%Y/%m', verbose_name=u'Фото товара')

    class Meta:
        verbose_name = u'Дополнительное изображение'
        verbose_name_plural = u'Дополнительные изображения'


class Properties(models.Model):
    """
    Свойства товаров
    """
    propName = models.CharField(max_length=100, verbose_name=u'Свойство', blank=True)
    category = models.ManyToManyField(Category, blank=True, null=True)

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


class CartItem(models.Model):
    """
    Корзина товаров
    """
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Item, unique=False)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    def total(self):
        return int(self.quantity) * int(self.product.price)

    def title(self):
        return self.product.title

    def image(self):
        return self.product.image

    @property
    def price(self):
        return self.product.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save()


class BaseOrderInfo(models.Model):
    """
    Базовая модель заказа, которая будет наследоваться другими моделями
    """

    class Meta:
        abstract = True

    # contat info
    email = models.EmailField(max_length=50, verbose_name=u'E-mail', blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name=u'Телефон')
    first_name = models.CharField(max_length=50, verbose_name=u'Имя')
    last_name = models.CharField(max_length=50, verbose_name=u'Фамилия', blank=True, null=True)
    call_time = models.CharField(max_length=50, verbose_name=u'Удобное время для звонка', blank=True, null=True)

    # shiping method
    ship_method = models.CharField(max_length=50, verbose_name=u'Способ доставки')

    # shiping address
    flat = models.CharField(max_length=100, verbose_name=u'Квартира', blank=True, null=True)
    building = models.CharField(max_length=100, verbose_name=u'Дом', blank=True, null=True)
    street = models.CharField(max_length=100, verbose_name=u'Улица', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name=u'Город')
    region = models.CharField(max_length=100, verbose_name=u'Область')
    office = models.CharField(max_length=100, verbose_name=u'Номер склада (адрес офиса)', blank=True, null=True)
    additional_info = models.CharField(max_length=100, verbose_name=u'№ подъезда, код на двери, этаж...', blank=True,
                                       null=True)

    # order comment
    comment = models.TextField(max_length=3000, verbose_name=u'Значение', blank=True, null=True)


class Order(BaseOrderInfo):
    # order status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPED = 3
    CANCELLED = 4
    # set order status
    ORDER_STATUS = (
        (SUBMITTED, 'Принято'),
        (PROCESSED, 'Обработанно'),
        (SHIPED, 'Доставлено'),
        (CANCELLED, 'Отменено'),
    )
    # order info
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата')
    status = models.IntegerField(choices=ORDER_STATUS, default=SUBMITTED, verbose_name=u'Статус заказа')
    ip_address = models.IPAddressField(blank=True, null=True, verbose_name=u'ip-адрес заказчика')
    last_updated = models.DateTimeField(auto_now=True, verbose_name=u'Последнее обновление')
    # user = models.ForeignKey(User, null=True) # возможно добавится в будущем

    def __unicode__(self):
        return u'Заказ № %s' % str(self.id)

    @property
    # http://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work
    # зачем сделано через property?
    def total(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'


class OrderItem(models.Model):
    product = models.ForeignKey(Item)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order)

    @property
    def total(self):
        return self.quantity * self.price

    @property
    def name(self):
        return self.product.name

    def __unicode__(self):
        return self.product.title

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    class Meta:
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'