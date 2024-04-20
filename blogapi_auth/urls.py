from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_login, name='login'),
    path('login', views.auth_login, name='login-route'),
    path('signup', views.auth_signup, name='signup'),
    path('logout', views.auth_logout, name='logout')
]