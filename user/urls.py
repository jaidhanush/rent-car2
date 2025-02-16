from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("admin/register/", AdminRegisterAPIView.as_view(), name="admin-register"),
    path("admin/login/", AdminLoginAPIView.as_view(), name="admin-login"),
    path('get-all-users/', GetAllUsers.as_view(), name='get-all-users'),
]
