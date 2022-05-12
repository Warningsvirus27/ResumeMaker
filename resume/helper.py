from datetime import date
from .models import *
from django.contrib import messages
from django.shortcuts import redirect


def year_list():
    years = []
    for index in range(80):
        years.append(date.today().year - index)
    return years


def get_resume_instance(request, resume):
    try:
        resume_instance = Resume.objects.get(id=resume)
    except Resume.DoesNotExist:
        messages.error(request, 'Invalid Resume ID')
        messages.error(request, 'Please try again !!!')
        return redirect('home')
    return resume_instance
