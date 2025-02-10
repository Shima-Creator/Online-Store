from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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