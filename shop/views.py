# coding: utf-8

import decimal
import random
from datetime import datetime, timedelta

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, mail_managers
from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models import Q, Max
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect

# local
from shop.models import Category, Item, ItemProperties, Images, Manufacturer, CartItem, HomeSlider
from shop.forms import ProductAddToCartForm, DivErrorList, Checkout
from decorators import render_to
from shop import cart


@render_to('shop/index.html')
def index(request):
    items = Item.objects.filter(publicated=True).order_by('-date')[:6]
    sliders = HomeSlider.objects.all()

    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    cart_item_count = CartItem.objects.filter(cart_id=_cart_id(request)).count()

    return {'items': items, 'categories': categories, 'manufacturers': manufacturers, 'cart_item_count': cart_item_count,
            'sliders': sliders}


@render_to('shop/products.html')
def category_page(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    items = Item.objects.filter(publicated=True, category=category.pk).order_by('-date')

    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    if 'order' in request.GET:
        order = request.GET.get('order')
        if order == 'low':
            items.order_by('price')
        if order == 'high':
            items.order_by('-price')

    # pagination
    items = pagination(request, items)

    return {'items': items, 'category': category, 'categories': categories, 'manufacturers': manufacturers}


@render_to('shop/products.html')
def manufacturer_page(request, slug=None):
    manufacturer = get_object_or_404(Manufacturer, slug=slug)
    items = Item.objects.filter(publicated=True, manufacturer=manufacturer.pk).order_by('-date')

    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    if 'order' in request.GET:
        order = request.GET.get('order')
        if order == 'low':
            items.order_by('price')
        if order == 'high':
            items.order_by('-price')

    # pagination
    items = pagination(request, items)

    return {'items': items, 'category': manufacturer, 'categories': categories, 'manufacturers': manufacturers}


@render_to('shop/product-details.html')
def item(request, self_slug, category_slug):
    item = get_object_or_404(Item, slug=self_slug, category__slug=category_slug)

    items = Item.objects.filter(publicated=True, category__slug=category_slug).exclude(slug=self_slug)[:12]

    form = ProductAddToCartForm(request=request, label_suffix=':')
    success = ''
    if request.method == 'POST':
        # TODO refactoring
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata, error_class=DivErrorList)
        if form.is_valid():
            cart.add_to_cart(request)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            success = 'Товар добавлен в корзину.'
        else:
            print 'form not valid'

    form.fields['product_slug'].widget.attrs['value'] = self_slug
    request.session.set_test_cookie()
    cart_item_count = CartItem.objects.filter(cart_id=_cart_id(request)).count()

    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    return {'item': item, 'items': items, 'success': success, 'form': form, \
            'cart_item_count': cart_item_count, 'categories': categories, 'manufacturers': manufacturers}


@render_to('shop/cart.html')
def show_cart(request):
    cart_item_count = CartItem.objects.filter(cart_id=_cart_id(request)).count()
    cart_items = CartItem.objects.filter(cart_id=_cart_id(request))

    cart_subtotal = decimal.Decimal('0.00')
    if cart_items:
        for item in cart_items:
            cart_subtotal += int(item.product.price) * int(item.quantity)

    return {'cart_items': cart_items,
            'cart_subtotal': cart_subtotal,
            'cart_item_count': cart_item_count}


def add_to_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(product__id=item_id, cart_id=_cart_id(request))
        cart_item.augment_quantity(1)
    except ObjectDoesNotExist:
        item = Item.objects.get(id=item_id)
        CartItem.objects.create(product = item, cart_id=_cart_id(request))
    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def _cart_id(request):
    CART_ID_SESSION_KEY = 'cart_id'
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
        cart_id = ''
        for y in range(50):
            cart_id += characters[random.randint(0, len(characters) - 1)]
        request.session[CART_ID_SESSION_KEY] = cart_id
    return request.session[CART_ID_SESSION_KEY]


@render_to('shop/checkout.html')
def checkout(request):
    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('cart')
        return HttpResponseRedirect(cart_url)

    form = Checkout()
    if request.method == 'POST':
        form = Checkout(request.POST)
        if form.is_valid():
            checkout_form = form.save(commit=False)
            checkout_form.save()
            # отправка почты менеджеру
            manager_message = ''
            manager_message_title = u'Новый заказ №:%s' % checkout_form.id
            for field in form.fields:
                if form.cleaned_data[field]:
                    manager_message += "%s: %s\n" % (form.fields[field].label, form.cleaned_data[field])
            mail_managers(manager_message_title, manager_message)
            # отправка почты заказчику
            user_message = u'Спасибо за заказ.\n Номер заказа:%s' % checkout_form.id
            user_message_title = u'Спасибо за заказ'
            email = form.cleaned_data['email']
            if email:
                send_mail(user_message_title, user_message, u'Military shop', [email])

            CartItem.objects.filter(cart_id=_cart_id(request)).delete()

    cart_item_count = CartItem.objects.filter(cart_id=_cart_id(request)).count()
    cart_items = CartItem.objects.filter(cart_id=_cart_id(request))
    return {'cart_items': cart_items, 'form': form, 'cart_item_count': cart_item_count}


@render_to('shop/search.html')
def show_search(request):
    words = request.GET.get('words')
    error = True if words is None else ''
    items = Item.objects.filter(Q(title__icontains=words) |
                                Q(item_description__icontains=words) |
                                Q(description__icontains=words) |
                                Q(keywords__icontains=words)) if not error else ''
    # pagination
    items = pagination(request, items)
    random_item = Item.objects.order_by('?')[:4]

    return {'items': items,
            'random_item': random_item,
            'error': error,
            'words': words}


# -------------------------------------------- #
def pagination(request, items):
    paginator = Paginator(items, 9)  # показывать по 9 товаров на странице
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return items
# -------------------------------------------- #
