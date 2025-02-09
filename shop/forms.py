from django import forms
from .models import Product, Salesman


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['photo','name', 'description', 'shop','stock', 'price']


class SalesmanForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ['shop', 'country', 'category']