from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('/out/', views.logout, name='logout'),
    path('/forgot_password/', views.forgot_password, name='forgot_password'),
]
