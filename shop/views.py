# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, mail_managers
from django.core import urlresolvers
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect

from shop.models import Category, Item, Manufacturer, HomeSlider, Order, OrderedItems
from shop.forms import ProductAddToCartForm, Checkout
from decorators import render_to
from shop import cart


@render_to('shop/index.html')
def index(request):
    items = Item.objects.filter(publicated=True).order_by('-date')[:6]
    sliders = HomeSlider.objects.all()

    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    return {'items': items, 'categories': categories, 'manufacturers': manufacturers, \
            'cart_item_count': cart.distinct_item_count(request), 'sliders': sliders}


@render_to('shop/products.html')
def category_page(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    items = Item.objects.filter(publicated=True, category=category.pk).order_by('-date')

    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    # pagination
    items = pagination(request, items)

    return {'items': items, 'category': category, 'categories': categories, 'manufacturers': manufacturers, \
            'cart_item_count': cart.distinct_item_count(request)}


@render_to('shop/products.html')
def manufacturer_page(request, slug=None):
    manufacturer = get_object_or_404(Manufacturer, slug=slug)
    items = Item.objects.filter(publicated=True, manufacturer=manufacturer.pk).order_by('-date')

    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    # pagination
    items = pagination(request, items)

    return {'items': items, 'category': manufacturer, 'categories': categories, 'manufacturers': manufacturers, \
            'cart_item_count': cart.distinct_item_count(request)}


@render_to('shop/product-details.html')
def item(request, category_slug, self_slug):
    item = get_object_or_404(Item, slug=self_slug, category__slug=category_slug)
    items = Item.objects.filter(publicated=True, category__slug=category_slug).exclude(slug=self_slug)[:12]

    form = ProductAddToCartForm(request=request, label_suffix=':')
    if request.method == 'POST':
        form = ProductAddToCartForm(request, request.POST)
        if form.is_valid():
            cart.add_to_cart(request)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            request.success = True

    form.fields['product_slug'].widget.attrs['value'] = self_slug
    request.session.set_test_cookie()

    # sidebar
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    return {'item': item, 'items': items, 'form': form, 'cart_item_count': cart.distinct_item_count(request), \
            'categories': categories, 'manufacturers': manufacturers}


@render_to('shop/cart.html')
def show_cart(request):
    cart_items = cart.get_cart_items(request)
    cart_subtotal = cart.cart_subtotal(request)

    return {'cart_items': cart_items,
            'cart_subtotal': cart_subtotal,
            'cart_item_count': cart.distinct_item_count(request)}


def add_to_cart(request, item_slug):
    cart.add_to_cart(request, item_slug)
    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, item_id):
    cart.remove_from_cart(request, item_id)
    return redirect(request.META.get('HTTP_REFERER'))


@render_to('shop/checkout.html')
def checkout(request):
    # TODO need to create email temaplates for managers and clients
    if cart.is_empty(request):
        return HttpResponseRedirect(urlresolvers.reverse('cart'))

    form = Checkout()
    if request.method == 'POST':
        form = Checkout(request.POST)
        if form.is_valid():
            checkout_form = form.save(commit=False)
            checkout_form.save()

            # manager's mail
            manager_message = ''
            manager_message_title = u'Новый заказ №:%s' % checkout_form.id
            for field in form.fields:
                if form.cleaned_data.get(field):
                    manager_message += "%s: %s\n" % (form.fields.get(field).label, form.cleaned_data.get(field))
            mail_managers(manager_message_title, manager_message)

            # clien's mail
            email = form.cleaned_data['email']
            if email:
                user_message = u'Спасибо за заказ.\n Номер заказа:%s' % checkout_form.id
                user_message_title = u'Спасибо за заказ'
                send_mail(user_message_title, user_message, u'Military shop', [email])

            items = cart.get_cart_items(request)
            for i in items:
                order = Order.objects.get(id=checkout_form.id)
                OrderedItems.objects.create(order=order , product=i.product, quantity=i.quantity, price=i.total())
            items.delete()

    cart_items = cart.get_cart_items(request)
    return {'cart_items': cart_items, 'form': form, 'cart_item_count': cart.distinct_item_count(request)}


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
