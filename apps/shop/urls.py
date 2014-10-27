from django.conf.urls import url, patterns

from apps.shop import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<slug>[a-z,0-9,_,-]+)/?$', views.category_page, name='category'),
                       url(r'^manufacturers/(?P<slug>[a-z,0-9,_,-]+)/?$', views.manufacturer_page, name='manufacturer'),
                       url(r'^(?P<category_slug>[-\w]+)/(?P<self_slug>[-\w]+)/$', views.item, name='item'),
                       url(r'^/cart/', views.show_cart, name='cart'),
                       url(r'^/checkout/', views.show_checkout, name='checkout'),
                       url(r'^/search/', views.show_search, name='show_search')
)
