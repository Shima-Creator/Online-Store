from django.core.checks import register
from django import template
import shop.views as views
from shop.models import Basket

register = template.Library()

@register.simple_tag()
def add_product_to_basket():
    return Basket.objects.create()

@register.simple_tag()
def count_products_in_basket(user_id):
    return Basket.objects.filter(username_id=user_id).count()