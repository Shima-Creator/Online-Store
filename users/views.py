from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView

from .forms import LoginUserForm, UserCreateForm, SellerRegisterForm, BuyerRegisterForm
from .models import Seller, Buyer


class LoginUserView(APIView):
    def get(self, request):
        form = LoginUserForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginUserForm(request, data=request.data)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('start_page'))
            return render(request, 'users/login.html', {'form':form})
        return render(request, 'users/login.html', {'form':form})


class RegisterUserView(APIView):
    def get(self, request):
        user_form = UserCreateForm()
        seller_form = SellerRegisterForm()
        buyer_form = BuyerRegisterForm()
        data = {'user_form': user_form,
                'seller_form': seller_form,
                'buyer_form': buyer_form,
                'error': 'Ошибка создания профиля'}
        return render(request, 'users/register.html', data)

    def post(self, request):
        user_form = UserCreateForm(request.POST)
        seller_form = SellerRegisterForm(request.POST)
        buyer_form = BuyerRegisterForm(request.POST)
        is_seller_str = request.POST.get('is_seller')

        is_seller = False

        print(f"REQUEST_POST = {request.POST}")

        print(f"IS_SELLER = {is_seller}")

        if is_seller_str == 'true':
            is_seller = True
        else:
            is_seller = False

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_seller = is_seller
            user.save()

            if is_seller:
                seller = Seller(user=user)
                if seller_form.is_valid():
                    seller = seller_form.save(commit=False)
                    seller.user = user
                    seller.save()
                    login(request, user)
                    return HttpResponseRedirect(reverse('start_page'))
                else:
                    print(seller_form.errors)
                    user.delete()
                    data = {'user_form':user_form,
                            'seller_form':seller_form,
                            'buyer_form':buyer_form,
                            'error':'Ошибка создания профиля'}
                    return render(request, 'users/register.html', data)

            else:
                buyer = Buyer(user=user)
                if buyer_form.is_valid():
                    buyer = buyer_form.save(commit=False)
                    buyer.user = user
                    buyer.save()
                    login(request, user)
                    return HttpResponseRedirect(reverse('start_page'))
                else:
                    print(buyer_form.errors)
                    user.delete()
                    data = {'user_form':user_form,
                            'seller_form':seller_form,
                            'buyer_form':buyer_form,
                            'error':'Ошибка создания профиля',
                            'buyer_errors': buyer_form.errors}
                    return render(request, 'users/register.html', data)
        return redirect('users:login')


class LogoutUserView(APIView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('users:login'))
