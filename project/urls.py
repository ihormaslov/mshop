# coding: utf-8
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from shop.sitemap import *


admin.autodiscover()

sitemaps = {
#    'shop_items': SitemapItems,
#    'shop_categories': SitemapCategories,
#    'shop_manufacturer': SitemapManufacturer
}

urlpatterns = patterns('',
                       # Examples:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^ckeditor/', include('ckeditor.urls')),
                       url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
                       url(r'^$', 'shop.views.index', name='index'),
                       url(r'^shop/', include('shop.urls', ), name='shop'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
    )
