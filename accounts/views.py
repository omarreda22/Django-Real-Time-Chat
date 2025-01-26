from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import RegisterForm
from chat.models import ChatRoom

User = get_user_model()


@login_required(login_url="accounts:login")
def home(request):
    user = request.user
    rooms = ChatRoom.objects.filter(Q(sender=user) | Q(receiver=user))

    users_in_rooms = User.objects.filter(
        Q(sender__in=rooms) | Q(receiver__in=rooms)
    ).distinct()

    user_not_in_rooms = (
        User.objects.exclude(id__in=users_in_rooms).exclude(id=user.id).distinct()
    )

    username_list = list(user_not_in_rooms.values_list("username", flat=True))

    return render(request, "home.html", {"username_list": username_list})


def chat_room_create(request):
    if request.method == "POST":
        username = request.POST.get("username")
        get_user = get_object_or_404(User, username=username)
        new_room = ChatRoom.objects.create(sender=request.user, receiver=get_user)

        return redirect("chat:room", id=new_room.id)

    return redirect("accounts:home")


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
