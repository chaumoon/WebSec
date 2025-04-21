from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'Home'),
    path('/', views.home, name = 'Home'),
    path('login/', views.login, name = 'Login'),
    path('register/', views.register, name='Register'),
    path('forgot/', views.forgot, name = 'Forgot'),
    path('admin/', views.admin, name = 'Admin'),
    path('user/', views.user, name = 'User'),
    path('logout/', views.logout, name = 'Logout'),
]