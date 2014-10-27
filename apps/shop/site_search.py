# coding: utf-8
import urllib

from django.db.models import Q
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from models import Item


def get_search_url(request):
    return urlresolvers.reverse('show_search')


def get_matched(request):
    words = request.GET.get('search_inp')
    results = {}
    results['items'] = []
    for word in words:
        items = Item.objects.filter(Q(title__icontains=word) |
                                    Q(item_description__icontains=word) |
                                    Q(description__icontains=word) |
                                    Q(keywords__icontains=word)
        )
        results['items'] = items

    print(results)
    kwargs = {'results': results}
    print get_search_url(request) + "?%s" % words
    return HttpResponseRedirect(get_search_url(request) + "?%s" % words)


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = urllib.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)