# coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap

from shop.views import index
from shop import api

# from shop.sitemap import *

admin.autodiscover()

sitemaps = {
#    'shop_items': SitemapItems,
#    'shop_categories': SitemapCategories,
#    'shop_manufacturer': SitemapManufacturer
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^$', index, name='index'),
    url(r'^shop/', include('shop.urls', ), name='shop'),

    # API
    url(r'^api/shop/categories/', include(api.CategoryResource.urls()))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]
