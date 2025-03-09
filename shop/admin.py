from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_display_links = ['name',]
    ordering = ['name']
    list_editable = ['description']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(SubCategory)
class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'description', 'category']
    list_display_links = ['name']
    list_editable = ['description']
    search_fields = ['name']
    list_filter = ['category']
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['photo', 'name', 'description',
                    'price','shop', 'stock']
    list_display_links = ['name']
    list_editable = ['photo', 'description',
                    'price', 'stock']
    search_fields = ['name']
    list_filter = ['name', 'description', 'price', 'stock']
    list_per_page = 10

@admin.register(Shop)
class SalesmanAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'country','description', 'category']
    list_display_links = ['shop_name']
    list_editable = ['country', 'category', 'description']
    search_fields = ['shop_name']
    list_filter = ['shop_name', 'country', 'category']
    list_per_page = 10


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['username', 'product', 'quantity']
    list_display_links = ['username']
    list_per_page = 10