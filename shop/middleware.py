# coding=utf-8

from django.http import HttpResponseRedirect
from django.core import urlresolvers
# locals
from forms import SearchForm
from models import Category
from cart import cart_distinct_item_count


class LocaleMiddleware(object):
    def process_request(self, request):

        # search
        search_form = SearchForm(request.GET)
        if request.method == 'GET' and search_form.is_valid():
            if search_form.cleaned_data.get('search'):
                return HttpResponseRedirect(urlresolvers.reverse('show_search') + "?words=%s" % form_data)
        request.search_form = search_form

        # category menu
        categories = Category.objects.filter(publicated=True).order_by('order', 'title')
        request.categories = categories

        # cart distinct item count
        cart_item_count = cart_distinct_item_count(request)
        request.cart_item_count = cart_item_count
        # сумма товаров в корзине не обновляется после добавления товара. миддлеваре выполняется раньше формы