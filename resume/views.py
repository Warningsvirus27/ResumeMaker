from django.shortcuts import render, HttpResponse
from django.contrib import auth
from django.contrib.auth import get_user_model


def homepage(request):
    if request.user.is_authenticated:
        return HttpResponse("THis is homepage")
    else:
        return HttpResponse('Invalid entry')


def template_edit(request, template_id=None):
    user = request.user
    data = {'mail': user.get_username(), 'name': user.get_full_name()}

    return render(request, 'html/srt-resume.html', data)


def create_resume(request):
    return render(request, 'html/create_resume.html')
