from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import Buyer, Seller, User


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class SellerRegisterForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['upd', 'legal_name',]


class BuyerRegisterForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['address',]


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class':'form-input'}))
