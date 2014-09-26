from django.contrib import admin
from django.db import models
from django.forms import CheckboxInput

from apps.shop.models import Category, Item, ItemProperties, Properties


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'order', 'parent', 'publicated')}),
        ('SEO', {
            'classes': ('collapse', ),
            'fields': ('slug', 'keywords', 'description')})
    )


class ItemPropertiesInlines(admin.StackedInline):
    model = ItemProperties
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.BooleanField: {'widget': CheckboxInput}
    }
    list_display = ('title', 'category', 'price', 'date', 'action_item', 'add_in_slider', )
    list_editable = ('action_item', 'add_in_slider',)
    search_fields = ['title', 'item_description']
    prepopulated_fields = {'slug': ('title', )}

    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'price', 'image', 'date', 'inStore', 'publicated', 'action_item', 'order', 'item_description', )}),
        ('SEO', {
            'classes': ('collapse', ),
            'fields': ('slug', 'keywords', 'description', )})
    )
    inlines = [ItemPropertiesInlines]


class PropertiesAdmin(admin.ModelAdmin):
    list_display = ('propName', )
    fields = ('propName', 'category', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Properties, PropertiesAdmin)