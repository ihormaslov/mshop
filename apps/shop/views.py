# coding: utf-8

import json

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404

from apps.shop.models import Category, Item, ItemProperties


def index(request, slug=None, pk=None):
    """
    вывод товаров на главной странице
    """
    categories = Category.objects.filter(publicated=True).order_by('order', 'title')
    items = Item.objects.filter(publicated=True).prefetch_related('itemproperties_set').all().order_by('order', 'title')
    props = ItemProperties.objects.all().order_by('prop')
    action_items = Item.objects.filter(publicated=True, action_item=True)
    slider_items = Item.objects.filter(publicated=True, add_in_slider=True)
    if request.method == 'POST' and request.is_ajax():
        if 'filter-box' in request.POST:
            boxes = request.POST.getlist('filter-box', False)
            ids = ItemProperties.objects.filter(propValue__in=boxes).values_list('item_id', flat=True)

            items = Item.objects.filter(id__in=ids)\
                .prefetch_related('itemproperties_set').all()\
                .order_by('order', 'title')

            respons_items = []
            for it in items:
                permalink = it.get_absolute_url()
                p = list(it.itemproperties_set.all().values('prop__propName', 'propValue'))
                i = dict([('title', it.title), ('price', it.price), ('image', str(it.image)), ('item_description', it.item_description), ('item_url', permalink), ('props', p)])

                respons_items.append(i)

           # вывод json средствами django
           # items = serializers.serialize('json', items, indent=4)
           # l = serializers.serialize('json', l, indent=4)

          #  print items
          #  return HttpResponse(items)

            return HttpResponse(json.dumps(respons_items), 'application/json')
        else:
            print 'not POST'

    kwargs = {'context_instance': RequestContext(request)}

    return render_to_response('shop/index.html',
                              {'categories': categories,
                               'items': items,
                               'props': props,
                               'action_items': action_items,
                               'slider_items': slider_items}, **kwargs)


def category_page(request, slug=None):
    categories = Category.objects.filter(publicated=True).order_by('order', 'title')

    try:
        category = Category.objects.get(id=int(slug))
    except ValueError:
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404

    items = Item.objects.filter(publicated=True, category=category.pk).order_by('order')
    props = ItemProperties.objects.filter(prop__category=category.pk).order_by('prop')

    if request.method == 'POST' and request.is_ajax():
        if 'filter-box' in request.POST:
            boxes = request.POST.getlist('filter-box', False)
            ids = ItemProperties.objects.filter(propValue__in=boxes).values_list('item_id', flat=True)

            items = list(Item.objects.filter(id__in=ids).all().order_by('order', 'title').values('title', 'price', 'item_description', 'image'))

            return HttpResponse(json.dumps(items), 'application/json')
        else:
            print 'not POST'

    kwargs = {'context_instance': RequestContext(request)}

    return render_to_response('shop/category.html',
        {'items': items,
         'categories': categories,
         'props': props}, **kwargs)


def item(request, self_slug, category_slug):
    categories = Category.objects.filter(publicated=True).order_by('order', 'title')
    item_queryset = get_object_or_404(Item, slug=self_slug, category__slug=category_slug)

    kwargs = {'context_instance': RequestContext(request)}

    return render_to_response('shop/item.html',
        {'item': item_queryset,
         'categories': categories,}, **kwargs)
