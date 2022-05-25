from django.template.defaulttags import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),

    path('template_edit/', views.template_edit, name='template_edit'),
    path('edit<int:resume_id>', views.edit, name='edit'),
    path('edit', views.edit, name='edit'),

    path('create_new_resume', views.create_new_resume, name='create_new_resume'),
    path('create_resume<int:resume_id><str:field>', views.create_resume, name='create_resume'),
    path('create_resume<int:resume_id>', views.create_resume, name='create_resume'),
    path('preview<int:resume_id><str:template_name>', views.preview, name='preview'),
    path('download<int:resume><str:template_name>', views.download_template, name='download'),

    path('view_resume', views.view_resume, name='view_resume'),

    path('upload', views.upload, name='upload'),

    path('<str:user>/doc', views.document_check, name='document'),
]
