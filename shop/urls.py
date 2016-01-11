from django.conf.urls import url, include

from shop import views

urlpatterns = [
    # regular urls
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<slug>[a-z,0-9,_,-]+)/?$', views.category_page, name='category'),
    url(r'^(?P<category_slug>[-\w]+)/(?P<self_slug>[-\w]+)/$', views.item, name='item'),
    url(r'^manufacturer/(?P<slug>[a-z,0-9,_,-]+)/?$', views.manufacturer_page, name='manufacturer'),

    url(r'^cart/$', views.show_cart, name='cart'),
    url(r'^cart/remove/(?P<item_id>\d+)/', views.remove_from_cart, name='remove_from_cart'),
    url(r'^cart/add/(?P<item_slug>\w+)/', views.add_to_cart, name='add_to_cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),

    url(r'^search/$', views.show_search, name='show_search'),
]
