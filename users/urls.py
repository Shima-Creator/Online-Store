from users import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
]