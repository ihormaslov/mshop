# coding: utf-8
import random
from datetime import datetime, timedelta

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, mail_managers
from django.core import urlresolvers
from django.conf import settings
from django.db.models import Q, Max
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect

# local
from shop.models import Category, Item, ItemProperties, Images, Manufacturer, CartItem
from shop.forms import ProductAddToCartForm, DivErrorList, Checkout
from decorators import render_to
from shop import cart


@render_to('shop/index.html')
def index(request):
    items = Item.objects.filter(publicated=True).order_by('date')
    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    cart_item_count = cart.cart_distinct_item_count(request)

    return {'items': items, 'categories': categories, 'manufacturers': manufacturers, 'cart_item_count': cart_item_count}


@render_to('shop/products.html')
def category_page(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    items = Item.objects.filter(publicated=True, category=category.pk)

    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    order_by = '-date'
    if 'order' in request.GET:
        order = request.GET.get('order')
        if order == 'low':
            order_by = 'price'
        if order == 'high':
            order_by = '-price'

    # pagination
    items = pagination(request, items.order_by(order_by))

    return {'items': items, 'category': category, 'categories': categories, 'manufacturers': manufacturers}


def manufacturer_page(request, slug=None):
    """docstring for manufacturer_page"""
    pass


@render_to('shop/product-details.html')
def item(request, self_slug, category_slug):
    item = get_object_or_404(Item, slug=self_slug, category__slug=category_slug)

    items = Item.objects.filter(publicated=True, category__slug=category_slug).exclude(slug=self_slug)[:12]

    form = ProductAddToCartForm(request=request, label_suffix=':')
    success = ''
    if request.method == 'POST':
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
    cart_item_count = cart.cart_distinct_item_count(request)

    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    return {'item': item, 'items': items, 'success': success, 'form': form, \
            'cart_item_count': cart_item_count, 'categories': categories, 'manufacturers': manufacturers}


@render_to('shop/cart.html')
def show_cart(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
        if postdata['submit'] == 'Checkout':
            return HttpResponseRedirect(urlresolvers.reverse('checkout'))

    cart_item_count = cart.cart_distinct_item_count(request)
    cart_items = cart.get_cart_items(request)
    cart_subtotal = cart.cart_subtotal(request)

    return {'cart_items': cart_items,
            'cart_subtotal': cart_subtotal,
            'cart_item_count': cart_item_count}


def add_to_cart(request):
    """docstring for add_to_cart"""
    pass


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
def show_checkout(request):
    message = False
    # cart_item_count = ''

    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('cart')
        return HttpResponseRedirect(cart_url)

    if request.method == 'POST':
        postdata = request.POST.copy()
        form = Checkout(postdata, error_class=DivErrorList)
        if form.is_valid():
            checkout_form = form.save(commit=False)
            checkout_form.ip_address = request.META.get('REMOTE_ADDR')
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

            cart.empty_cart(request)
            message = True
    else:
        form = Checkout()
    cart_item_count = cart.cart_distinct_item_count(request)
    print cart_item_count
    return {'message': message,
            'form': form,
            'cart_item_count': cart_item_count}


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
