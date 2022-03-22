from django.shortcuts import render


def login(request):
    username = request.GET.get("username")
    password = request.GET.get("password")

    return render(request, 'html/login.html')


def logout(request):
    return render(request, 'html/logout.html')


def forgot_password(request):
    return render(request, 'html/forgot_password.html')



