from django import forms

from users.models import Seller
from .models import Product, Shop


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['photo','name', 'subcategory', 'description', 'stock', 'price']


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shop_name', 'country', 'category', 'description']


class SellerEditForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['profile_pic', 'facebook', 'instagram', 'vk', 'telegram']


