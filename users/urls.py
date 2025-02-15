from itertools import product

from debug_toolbar.urls import app_name
from django.contrib.auth.views import LogoutView
from pygments.lexer import include

from users import views

from django.urls import path

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
]

