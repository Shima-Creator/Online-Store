from django.http import HttpResponseRedirect

from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView


from .forms import LoginUserForm, RegisterUserForm


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
         form = RegisterUserForm()
         return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterUserForm(data=request.data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('start_page'))
        return render(request, 'users/login.html', {'form':form})


class LogoutUserView(APIView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('users:login'))