from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import ChatRoom
from .forms import ChatMessageForm


@login_required
def room(request, id):
    room = get_object_or_404(ChatRoom, pk=id)
    messages = room.chat_message.all()
    form = ChatMessageForm(request.POST or None)

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
    }
    return render(request, "chat/room.html", context)
