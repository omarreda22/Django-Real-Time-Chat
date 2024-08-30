from django.shortcuts import render


def home(request):
    return render(request, "home.html", {})


def user_login(request):
    return render(request, "accounts/login.html", {})
