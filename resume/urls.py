from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    path('template/<int:template_id>/', views.template_edit, name='template_edit'),
]
