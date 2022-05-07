from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('out/', views.logout, name='logout'),
    path('<str:email>/<str:index>/forgot_password/', views.forgot_password, name='forgot_password'),
    path('register/', views.register, name='register'),
    path('<str:user>/set_password/', views.set_password, name='set_password'),
    path('<str:user>/create_password/', views.create_password, name='create_password'),
    path('<str:email>change_password', views.change_password, name='change_password'),
]

