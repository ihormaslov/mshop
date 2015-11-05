# coding: utf-8
from django.contrib import admin
from django.db import models
from django.forms import CheckboxInput

from shop.models import Category, Item, ItemProperties, Properties, Images, Order, OrderedItems, Manufacturer, HomeSlider


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (None, {
            'fields': ('name', 'order', 'parent', 'publicated')}),
        ('SEO', {
            'classes': ('collapse', ),
            'fields': ('slug', 'keywords', 'description')})
    )


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (None, {
            'fields': ('name', 'order', 'publicated')}),
        ('SEO', {
            'classes': ('collapse', ),
            'fields': ('slug', 'keywords', 'description')})
    )


class ItemPropertiesInlines(admin.StackedInline):
    model = ItemProperties
    extra = 1


class ImagesInlines(admin.StackedInline):
    model = Images
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.BooleanField: {'widget': CheckboxInput}
    }
    list_display = ('name', 'category', 'price', 'date', )
    search_fields = ['name', 'item_description']
    prepopulated_fields = {'slug': ('name', )}

    inlines = [ImagesInlines, ItemPropertiesInlines]

    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'price', 'manufacturer',
                       'in_store', 'publicated', 'order', 'item_description', 'date',)}),
        ('SEO', {
            'classes': ('collapse', ),
            'fields': ('slug', 'keywords', 'description', )})
    )


class PropertiesAdmin(admin.ModelAdmin):
    list_display = ('propName', )
    fields = ('propName', 'category', 'order', )


class OrderItemInline(admin.StackedInline):
    model = OrderedItems
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status', 'total',)
    search_fields = ('email', 'ship_method', 'phone', )
    inlines = [OrderItemInline]

    fieldsets = (
        (u'Основное', {'fields': ('status', 'email', 'phone', 'first_name', 'last_name', 'ship_method',)}),
        (u'Комментарий к заказу', {'fields': ('comment',)}),
    )


class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('name', 'link',)
    fields = ('name', 'image', 'link', 'text',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Properties, PropertiesAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(HomeSlider, HomeSliderAdmin)
