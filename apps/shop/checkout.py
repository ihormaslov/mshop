# coding: UTF-8

from django.core import urlresolvers
from django.core.mail import send_mail

import cart
from models import Order, OrderItem



# returns the URL from the checkout module for cart
def get_checkout_url(request):
    return urlresolvers.reverse('checkout')


def create_order(request, postdata):
    order = Order()

    # order.user = None
    # if request.user.is_authenticated():
    # order.user = request.user

    # данные с формы
    data = {
        u'Имя': postdata['first-name'],
        u'Фамилия': postdata['last-name'],
        u'Email': postdata['email'],
        u'Телефон': postdata['phone'],
        u'Время звонка': postdata['call-time'],
        u'Область': postdata['region'],
        u'Город': postdata['city'],
        u'Улица': postdata['street'],
        u'Дом': postdata['building'],
        u'Квартира': postdata['flat'],
        u'Способ доставки': postdata['ship-method'],
        u'Номер склада (адрес офиса)': postdata['warehouse'],
        u'Комментарий к заказу': postdata['comment'],
        u'Дополнительная информация': postdata['additional_info'],

    }

    # добавление данных в модель заказа
    order.first_name = data[u'Имя']
    order.last_name = data[u'Фамилия']
    order.email = data[u'Email']
    order.phone = data[u'Телефон']
    order.call_time = data[u'Время звонка']
    order.region = data[u'Область']
    order.city = data[u'Город']
    order.street = data[u'Улица']
    order.building = data[u'Дом']
    order.flat = data[u'Квартира']
    order.ship_method = data[u'Способ доставки']
    order.office = data[u'Номер склада (адрес офиса)']
    order.additional_info = data[u'Дополнительная информация']
    order.comment = data[u'Комментарий к заказу']
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.status = Order.SUBMITTED
    order.save()
    # отправка почты менеджеру
    send_mail_manager(data, order)
    # отправка почты заказчкику
    if data[u'Email'] != '':
        send_mail_customer(data, order)
    # if the order save succeeded
    if order.pk:
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            # create order item for each cart item
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price  # now using @property
            oi.product = ci.product
            oi.save()
        # all set, empty cart
        cart.empty_cart(request)
        # return the new order object
        # return order


def send_mail_manager(data, order):
    subject = u'Заказ № ' + str(order.id)
    mail_message = ''
    for t, v in data.iteritems():
        if v != '':
            mail_message += t + ': ' + v + '<br/>'

    send_mail(
        subject,
        mail_message,
        'Military Shop',
        ['maslov.ihor@gmail.com']
    )


def send_mail_customer(data, order):
    subject = u'Заказ № ' + str(order.id)
    mail_message = u'<h2>Спасибо за заказ!</h2>' \
                   u'<h3>Наш менеджер свяжется с вами в ближайшее время</h3>' \
                   u'Номер вашего заказа: ' + str(order.id)
    send_mail(
        subject,
        mail_message,
        'Military Shop',
        [data[u'Email']]
    )