import decimal  # not needed yet but we will later
import random
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Max
from django.shortcuts import get_object_or_404

from models import CartItem
from models import Item as Product


CART_ID_SESSION_KEY = 'cart_id'


# get the current user's cart id, sets new one if blank
# TODO to be removed
def _cart_id(request):
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
        cart_id = ''
        for y in range(50):
            cart_id += characters[random.randint(0, len(characters) - 1)]
        request.session[CART_ID_SESSION_KEY] = cart_id
    return request.session[CART_ID_SESSION_KEY]


# return all items from the current user's cart
def get_cart_items(request):
    return CartItem.objects.filter(cart_id=_cart_id(request))


# add an item to the cart
def add_to_cart(request):
    product_slug = request.POST.get('product_slug', '')
    quantity = request.POST.get('quantity', 1)
    p = get_object_or_404(Product, slug=product_slug)
    cart_products = CartItem.objects.filter(cart_id=_cart_id(request))
    product_in_cart = False
    for cart_item in cart_products:
        if cart_item.product.id == p.id:
            cart_item.augment_quantity(quantity)
            product_in_cart = True

    if not product_in_cart:
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()


# returns the total number of items in the user's cart
def cart_distinct_item_count(request):
    return get_cart_items(request).count()


def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))


# update quantity for single item
def update_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            remove_from_cart(request)


# remove a single item from cart
# TODO to be remover
def remove_from_cart(request):
    item_id = request.POTS.get('item_id')
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


# gets the total cost for the current cart
def cart_subtotal(request):
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += int(cart_item.product.price) * int(cart_item.quantity)
    return cart_total


def is_empty(request):
    return cart_distinct_item_count(request) == 0


def empty_cart(request):
    user_cart = get_cart_items(request)
    user_cart.delete()


# removing ild carts
def remove_old_cart_items():
    print "Removing old carts"
    # calculate date of SESSION_AGE_DAYS days ago
    remove_before = datetime.now() + timedelta(days=-settings.SESSION_AGE_DAYS)
    cart_ids = []
    old_items = CartItem.objects.values('cart_id'). \
        annotate(last_change=Max('date_added')). \
        filter(last_change__lt=remove_before).order_by()
    # create a list of cart IDs that havent been modified
    for item in old_items:
        cart_ids.append(item['cart_id'])
    to_remove = CartItem.objects.filter(cart_id__in=cart_ids)
    # delete those CartItem instances
    to_remove.delete()
    print str(len(cart_ids)) + " carts were removed"
