# coding: utf-8
from django.contrib import admin
from django.db import models
from django.forms import CheckboxInput

from apps.shop.models import Category, Item, ItemProperties, Properties, Manufacturer, AdditionalImages, Order, \
    OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'order', 'parent', 'publicated')}),
        ('SEO', {
            'classes': ('collapse', ),
            'fields': ('slug', 'keywords', 'description')})
    )


class ItemPropertiesInlines(admin.StackedInline):
    model = ItemProperties
    extra = 1


class AdditionalImageInlines(admin.StackedInline):
    model = AdditionalImages
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.BooleanField: {'widget': CheckboxInput}
    }
    list_display = ('title', 'category', 'manufacturer', 'old_price', 'price', 'date', 'action_item', )
    list_editable = ('action_item',)
    search_fields = ['title', 'item_description']
    prepopulated_fields = {'slug': ('title', )}

    fieldsets = (
        (None, {
            'fields': ('category', 'manufacturer', 'title', 'old_price', 'price', 'image', 'date',
                       'inStore', 'publicated', 'action_item', 'order', 'item_description', )}),
        ('SEO', {
            'classes': ('collapse', ),
            'fields': ('slug', 'keywords', 'description', )})
    )

    inlines = [AdditionalImageInlines, ItemPropertiesInlines]


class PropertiesAdmin(admin.ModelAdmin):
    list_display = ('propName', )
    fields = ('propName', 'category', )


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('country_name',)
    prepopulated_fields = {'slug': ('country_name',)}

    fieldsets = (
        (None, {
            'fields': ('country_name', 'order', 'logo', 'image')}),
        ('SEO', {
            'classes': ('collapse', ),
            'fields': ('slug', 'keywords', 'description')})
    )


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status', 'total',)
    search_fields = ('email', 'ship_method', 'phone', )
    inlines = [OrderItemInline]

    fieldsets = (
        (u'Основное', {'fields': ('status', 'email', 'phone', 'first_name', 'last_name',)}),
        (u'Доставка',
         {'fields': ('ship_method', 'office', 'region', 'city', 'street', 'building', 'flat', 'additional_info',)}),
        (u'Комментарий к заказу', {'fields': ('comment',)}),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Properties, PropertiesAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Order, OrderAdmin)