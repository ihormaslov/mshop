# coding: utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404

from apps.shop.models import Category, Item, ItemProperties, Manufacturer, AdditionalImages

# imports for cart
import cart
import checkout
from django.http import HttpResponseRedirect
from django.core import urlresolvers
from forms import ProductAddToCartForm, DivErrorList
# end imports for cart

# search
from django.db.models import Q

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request, slug=None, pk=None):
    """
    вывод товаров на главной странице
    """
    categories = Category.objects.filter(publicated=True).order_by('order', 'title')
    manufactures = Manufacturer.objects.all()
    items = Item.objects.filter(publicated=True).prefetch_related('itemproperties_set').all().order_by('order',
                                                                                                       'title')[:12]
    items_latest = Item.objects.filter(publicated=True).prefetch_related('itemproperties_set').all() \
                       .order_by('date')[:12]
    props = ItemProperties.objects.all().order_by('prop')
    action_items = Item.objects.filter(publicated=True, action_item=True)

    cart_item_count = cart.cart_distinct_item_count(request)
    kwargs = {'context_instance': RequestContext(request)}

    # search
    if request.method == 'GET' and 'search_inp' in request.GET:
        search_url = urlresolvers.reverse('show_search')
        words = request.GET.get('search_inp')
        return HttpResponseRedirect(search_url + "?words=%s" % words)

    return render_to_response('shop/index.html',
                              {'categories': categories,
                               'items': items,
                               'items_latest': items_latest,
                               'cart_item_count': cart_item_count,
                               'props': props,
                               'action_items': action_items,
                               'manufactures': manufactures, }, **kwargs)


def category_page(request, slug=None):
    categories = Category.objects.filter(publicated=True).order_by('order', 'title')
    manufactures = Manufacturer.objects.all()
    try:
        category = Category.objects.get(id=int(slug))
    except ValueError:
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404

    items = Item.objects.filter(publicated=True, category=category.pk).order_by('order', '-date')
    random_item = Item.objects.order_by('?')[:4]
    props = ItemProperties.objects.filter(prop__category=category.pk).values('prop__propName', 'prop__pk',
                                                                             'propValue').distinct().order_by('prop')

    boxes = ''
    manuf = ''
    if request.method == 'POST':
        if 'reset' not in request.POST:
            ids_prop = []
            ids_manuf = []
            # фильтрация по свойствам товара
            if 'filter-box' in request.POST:
                boxes = request.POST.getlist('filter-box', False)
                ids_prop = ItemProperties.objects.filter(propValue__in=boxes).values_list('item_id', flat=True)
            else:
                print 'no filter checked'

            # фильтрация по производителям
            if 'manuf-box' in request.POST:
                manuf = request.POST.getlist('manuf-box', False)
                manuf_id = Manufacturer.objects.filter(country_name__in=manuf).values_list('id', flat=True)
                ids_manuf = Item.objects.filter(publicated=True, manufacturer=manuf_id).values_list('id', flat=True)
            else:
                print 'no manuf checked'
            # фильтрация списка товаров
            print(list(ids_prop), list(ids_manuf))
            if len(ids_prop) == 0:
                ids = ids_manuf
            elif len(ids_manuf) == 0:
                ids = ids_prop
            else:
                ids = [e for e in ids_manuf if e in ids_prop]  # выбор одинаковых id товара со списков

                # ids = list(ids_prop) + list(ids_manuf)
            items = Item.objects.filter(publicated=True, id__in=ids, category=category.pk).all().order_by('order',
                                                                                                          'title')

    # pagination
    paginator = Paginator(items, 9)  # показывать по 9 товаров на странице
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    cart_item_count = cart.cart_distinct_item_count(request)
    kwargs = {'context_instance': RequestContext(request)}

    # search
    if request.method == 'GET' and 'search_inp' in request.GET:
        search_url = urlresolvers.reverse('show_search')
        words = request.GET.get('search_inp')
        return HttpResponseRedirect(search_url + "?words=%s" % words)

    return render_to_response('shop/products.html',
                              {'items': items,
                               'manufactures': manufactures,
                               'categories': categories,
                               'category': category,
                               'cart_item_count': cart_item_count,
                               'checked': boxes,
                               'checked_manuf': manuf,
                               'random_item': random_item,
                               'props': props}, **kwargs)


def item(request, self_slug, category_slug):
    categories = Category.objects.filter(publicated=True).order_by('order', 'title')
    item_queryset = get_object_or_404(Item, slug=self_slug, category__slug=category_slug)
    additional_images = AdditionalImages.objects.filter(item=item_queryset.pk)
    props = ItemProperties.objects.filter(item=item_queryset.pk).order_by('prop')
    random_item = Item.objects.order_by('?')[:4]

    items = Item.objects.filter(publicated=True, category__slug=category_slug).prefetch_related('itemproperties_set') \
                .all().exclude(slug=self_slug).order_by('order', 'title')[:12]

    # need to evaluate the HTTP method
    success = ''
    if request.method == 'POST':
        # add to cart...create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata, error_class=DivErrorList)
        # check if posted data is valid
        if form.is_valid():
            print('form valid')
            # add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            # url = urlresolvers.reverse('cart')
            # return HttpResponseRedirect(url)
            success = 'Товар добавлен в корзину.'
        else:
            print('form not valid')
    else:
        # its a GET, create the unbound form. Note request as a kwarg
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = self_slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()

    cart_item_count = cart.cart_distinct_item_count(request)
    kwargs = {'context_instance': RequestContext(request)}

    # search
    if request.method == 'GET' and 'search_inp' in request.GET:
        search_url = urlresolvers.reverse('show_search')
        words = request.GET.get('search_inp')
        return HttpResponseRedirect(search_url + "?words=%s" % words)

    return render_to_response('shop/product_detail.html',
                              {'item': item_queryset,
                               'additional_images': additional_images,
                               'props': props,
                               'items': items,
                               'success': success,
                               'cart_item_count': cart_item_count,
                               'form': form,
                               'random_item': random_item,
                               'categories': categories, }, **kwargs)


def manufacturer_page(request, slug=None):
    categories = Category.objects.filter(publicated=True).order_by('order', 'title')

    try:
        manufact = Manufacturer.objects.get(id=int(slug))
    except ValueError:
        try:
            manufact = Manufacturer.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404

    items = Item.objects.filter(publicated=True, manufacturer=manufact.pk).order_by('order', '-date')
    random_item = Item.objects.order_by('?')[:4]
    props = ItemProperties.objects.all().values('prop__propName', 'prop__pk', 'propValue').distinct().order_by('prop')

    boxes = ''
    if request.method == 'POST':
        if 'reset' not in request.POST:
            ids = []
            # фильтрация по свойствам товара
            if 'filter-box' in request.POST:

                boxes = request.POST.getlist('filter-box', False)
                ids = ItemProperties.objects.filter(propValue__in=boxes).values_list('item_id', flat=True)
            else:
                print 'no filter checked'

            items = Item.objects.filter(publicated=True, id__in=ids, manufacturer=manufact.pk).all().order_by('order',
                                                                                                              'title')

    # pagination
    paginator = Paginator(items, 9)  # показывать по 9 товаров на странице
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    cart_item_count = cart.cart_distinct_item_count(request)
    kwargs = {'context_instance': RequestContext(request)}

    # search
    if request.method == 'GET' and 'search_inp' in request.GET:
        search_url = urlresolvers.reverse('show_search')
        words = request.GET.get('search_inp')
        return HttpResponseRedirect(search_url + "?words=%s" % words)

    return render_to_response('shop/manufacturer.html',
                              {'items': items,
                               'checked': boxes,
                               'random_item': random_item,
                               'cart_item_count': cart_item_count,
                               'props': props,
                               'manuf': manufact,
                               'categories': categories, }, **kwargs)


def show_cart(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'RemoveAll':
            cart.empty_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
        if postdata['submit'] == 'Checkout':
            checkout_url = checkout.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)
    cart_items = cart.get_cart_items(request)
    cart_item_count = cart.cart_distinct_item_count(request)
    cart_subtotal = cart.cart_subtotal(request)
    random_item = Item.objects.order_by('?')[:4]
    kwargs = {'context_instance': RequestContext(request)}

    # search
    if request.method == 'GET' and 'search_inp' in request.GET:
        search_url = urlresolvers.reverse('show_search')
        words = request.GET.get('search_inp')
        return HttpResponseRedirect(search_url + "?words=%s" % words)

    return render_to_response('shop/cart.html', locals(), **kwargs)


def show_checkout(request):
    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        # вызов функции сохранения товаров
        checkout.create_order(request, postdata)
        # показывает сообщение, что заказ оформле
        message = True

    kwargs = {'context_instance': RequestContext(request)}

    # search
    if request.method == 'GET' and 'search_inp' in request.GET:
        search_url = urlresolvers.reverse('show_search')
        words = request.GET.get('search_inp')
        return HttpResponseRedirect(search_url + "?words=%s" % words)

    return render_to_response('shop/checkout.html', locals(), **kwargs)


def show_search(request):
    # search

    words = request.GET.get('words')

    if request.method == 'GET' and 'search_inp' in request.GET:
        search_url = urlresolvers.reverse('show_search')
        words = request.GET.get('search_inp')

    items = {}
    if words is None:
        error = True
    else:
        for word in words:
            items = Item.objects.filter(Q(title__icontains=word) |
                                        Q(item_description__icontains=word) |
                                        Q(description__icontains=word) |
                                        Q(keywords__icontains=word)
            )
        # pagination
        paginator = Paginator(items, 9)  # показывать по 9 товаров на странице

        page = request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

    random_item = Item.objects.order_by('?')[:4]

    return render_to_response('shop/search.html', locals(), context_instance=RequestContext(request))