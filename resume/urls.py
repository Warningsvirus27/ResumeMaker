from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    path('template/<int:template_id>/', views.template_edit, name='template_edit'),
    path('create_resume<int:resume_id><str:field>', views.create_resume, name='create_resume'),
    path('create_resume<int:resume_id>', views.create_resume, name='create_resume'),
    path('create_new_resume', views.create_new_resume, name='create_new_resume'),
]
