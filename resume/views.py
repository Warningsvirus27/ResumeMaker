from django.shortcuts import render, HttpResponse
from django.contrib import auth


def homepage(request):
    if request.user.is_authenticated:
        return HttpResponse("THis is homepage")
    else:
        return HttpResponse('Invalid entry')
