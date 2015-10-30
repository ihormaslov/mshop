import decimal  # not needed yet but we will later
import random
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Max
from django.shortcuts import get_object_or_404

from models import CartItems
from models import Item


CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):
    ''' get the current user's cart id, sets new one if blank '''
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
        cart_id = ''
        for y in range(50):
            cart_id += characters[random.randint(0, len(characters) - 1)]
        request.session[CART_ID_SESSION_KEY] = cart_id
    return request.session[CART_ID_SESSION_KEY]


def add_to_cart(request, item_slug=None):
    if item_slug:
        cart_item = CartItems.objects.filter(product__slug=item_slug, cart_id=_cart_id(request))
        if cart_item.exists():
            cart_item[0].augment_quantity(1)
        else:
            item = get_object_or_404(Item, slug=item_slug)
            CartItems.objects.create(product=item, cart_id=_cart_id(request))
    else:
        item_slug = request.POST.get('product_slug', '')
        quantity = request.POST.get('quantity', 1)
        cart_item = CartItems.objects.filter(product__slug=item_slug, cart_id=_cart_id(request))
        if cart_item.exists():
            cart_item[0].augment_quantity(1)
        else:
            item = get_object_or_404(Item, slug=item_slug)
            CartItems.objects.create(product=item, quantity=quantity, cart_id=_cart_id(request))


def remove_from_cart(request, item_id):
    get_object_or_404(CartItems, id=item_id, cart_id=_cart_id(request)).delete()


# update quantity for single item
# def update_cart(request):
#     postdata = request.POST.copy()
#     item_id = postdata['item_id']
#     quantity = postdata['quantity']
#     cart_item = get_object_or_404(CartItems, id=item_id, cart_id=_cart_id(request))
#     if cart_item:
#         if int(quantity) > 0:
#             cart_item.quantity = int(quantity)
#             cart_item.save()
#         else:
#             remove_from_cart(request)


def get_cart_items(request):
    return CartItems.objects.filter(cart_id=_cart_id(request))


def distinct_item_count(request):
    ''' returns the total number of items in the user's cart '''
    return CartItems.objects.filter(cart_id=_cart_id(request)).count()


# gets the total cost for the current cart
def cart_subtotal(request):
    total = decimal.Decimal('0.00')
    items = CartItems.objects.filter(cart_id=_cart_id(request))
    for item in items:
        total += item.total()
    return total


def is_empty(request):
    return distinct_item_count(request) == 0


def empty_cart(request):
    user_cart = CartItems.objects.filter(cart_id=_cart_id(request))
    user_cart.delete()


# removing old carts
def remove_old_cart_items():
    print "Removing old carts"
    # calculate date of SESSION_AGE_DAYS days ago
    remove_before = datetime.now() + timedelta(days=-settings.SESSION_AGE_DAYS)
    cart_ids = []
    old_items = CartItems.objects.values('cart_id'). \
        annotate(last_change=Max('date_added')). \
        filter(last_change__lt=remove_before).order_by()
    # create a list of cart IDs that havent been modified
    for item in old_items:
        cart_ids.append(item['cart_id'])
    to_remove = CartItems.objects.filter(cart_id__in=cart_ids)
    # delete those CartItems instances
    to_remove.delete()
    print str(len(cart_ids)) + " carts were removed"
