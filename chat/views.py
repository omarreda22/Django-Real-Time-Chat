from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Max
from django.db.models import OuterRef, Subquery

from .models import ChatRoom, ChatMessage
from .forms import ChatMessageForm


@login_required(login_url="accounts:login")
def room(request, id):
    room = get_object_or_404(ChatRoom, pk=id)
    user = request.user

    if user != room.sender and user != room.receiver:
        return redirect("accounts:home")

    messages = room.chat_message.all()
    form = ChatMessageForm(request.POST or None)
    user = request.user

    rooms = ChatRoom.objects.filter(Q(sender=user) | Q(receiver=user))
    rooms = rooms.annotate(new_message=Max("chat_message__created"))
    rooms = rooms.order_by("-new_message")

    get_last_message = ChatMessage.objects.filter(room=OuterRef("pk")).order_by(
        "-created"
    )

    rooms = rooms.annotate(
        last_message=Subquery(get_last_message.values("message")[:1]),
        created_time=Subquery(get_last_message.values("created")[:1]),
    )

    if request.htmx:
        message = form.save(commit=False)
        message.user = request.user
        message.room = room
        message.save()
        context = {"message": message, "user": request.user}
        return render(request, "chat/htmx/room_p.html", context)

    context = {
        "messages": messages,
        "form": form,
        "room": room,
        "rooms": rooms,
    }
    return render(request, "chat/room.html", context)


@login_required(login_url="accounts:login")
def room_list(request):
    user = request.user

    rooms = ChatRoom.objects.filter(Q(sender=user) | Q(receiver=user))
    rooms = rooms.annotate(new_message=Max("chat_message__created"))
    rooms = rooms.order_by("-new_message")

    get_last_message = ChatMessage.objects.filter(room=OuterRef("pk")).order_by(
        "-created"
    )

    rooms = rooms.annotate(
        last_message=Subquery(get_last_message.values("message")[:1]),
        created_time=Subquery(get_last_message.values("created")[:1]),
    )

    context = {
        "messages": [],
        "form": "form",
        "room": "room",
        "rooms": rooms,
    }

    return render(request, "chat/room.html", context)
