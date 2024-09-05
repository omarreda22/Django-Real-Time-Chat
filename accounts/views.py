from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages

from .forms import RegisterForm

User = get_user_model()


def home(request):
    return render(request, "home.html", {})


def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        get_user = User.objects.filter(email__iexact=email).distinct()
        if not get_user.exists():
            messages.error(request, "This User Doesn't Exist")
            return redirect("accounts:login")

        user = get_user.first()
        if not user.check_password(password):
            messages.error(request, "Wrong Password")
            return redirect("accounts:login")

        login(request, user)
        return redirect("accounts:home")

    return render(request, "accounts/login.html", {})


def user_logout(request):
    logout(request)
    messages.success(request, "Back Soon!")
    return redirect("accounts:login")


def user_register(request):
    form = RegisterForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.save()
        return redirect("accounts:login")

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)
