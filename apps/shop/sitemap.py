# coding: utf-8
from django.contrib.sitemaps import Sitemap

from models import Category, Item, Manufacturer


class SitemapItems(Sitemap):
    # Частота обновления страницы (см. http://www.sitemaps.org/)
    changfreq = 'weekle'
    # Приоритет сканирования страницы (см. http://www.sitemaps.org/)
    priority = 0.5

    def items(self):
        # выбираем данные для построения сайтмап
        it = Item.objects.filter(publicated=True).order_by('id')
        return it

    def lastmod(self, obj):
        # Метод возвращает дату которая указывается в параметре lastmod
        # (см. http://www.sitemaps.org/)
        return obj.modified


class SitemapCategories(Sitemap):
    # Частота обновления страницы (см. http://www.sitemaps.org/)
    changfreq = 'weekle'
    # Приоритет сканирования страницы (см. http://www.sitemaps.org/)
    priority = 0.5

    def items(self):
        # выбираем данные для построения сайтмап
        it = Category.objects.filter(publicated=True).order_by('id')
        return it

    def lastmod(self, obj):
        # Метод возвращает дату которая указывается в параметре lastmod
        # (см. http://www.sitemaps.org/)
        return obj.modified


class SitemapManufacturer(Sitemap):
    # Частота обновления страницы (см. http://www.sitemaps.org/)
    changfreq = 'weekle'
    # Приоритет сканирования страницы (см. http://www.sitemaps.org/)
    priority = 0.5

    def items(self):
        # выбираем данные для построения сайтмап
        it = Manufacturer.objects.all().order_by('id')
        return it

    def lastmod(self, obj):
        # Метод возвращает дату которая указывается в параметре lastmod
        # (см. http://www.sitemaps.org/)
        return obj.modified