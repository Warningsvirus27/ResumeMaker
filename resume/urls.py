from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    path('template_edit<int:template_id>/', views.template_edit, name='template_edit'),
    path('create_resume<int:resume_id><str:field>', views.create_resume, name='create_resume'),
    path('create_resume<int:resume_id>', views.create_resume, name='create_resume'),
    path('create_new_resume', views.create_new_resume, name='create_new_resume'),
    path('view_template', views.create_resume, name='template'),
    path('view_template<int:resume>', views.create_resume, name='template'),
    path('template', views.template, name='template'),
    path('template<int:resume>', views.template, name='template'),
    path('<str:requester>/<str:user>/doc', views.document_check, name='document'),
    path('<str:user>/doc', views.document_check, name='document'),
]
