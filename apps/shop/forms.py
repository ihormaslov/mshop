# coding: UTF-8
from django import forms
from django.forms.util import ErrorList


class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(label='Количество', widget=forms.TextInput(attrs={'size': '2',
                                                                                    'value': '1', 'class': 'span1',
                                                                                    'maxlength': '5'}),
                                  error_messages={'invalid': 'Введите правильное количество.'}, min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())

    # override the default __init__ so we can set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    # custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies должны быть включены.")
        return self.cleaned_data


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return u''
        return u'<div class="alert alert-warning" role="alert">%s</div>' % ''.join(
            [u'<div class="error">%s</div>' % e for e in self])