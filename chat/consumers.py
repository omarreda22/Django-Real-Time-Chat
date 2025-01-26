import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Q
from django.db.models import Max
from django.db.models import OuterRef, Subquery


from .models import ChatRoom, ChatMessage


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.chat_room_id = self.scope["url_route"]["kwargs"]["chatroom_id"]
        self.chat_room = get_object_or_404(ChatRoom, id=int(self.chat_room_id))

        async_to_sync(self.channel_layer.group_add)(
            self.chat_room_id, self.channel_name
        )

        # add user to online
        if self.user not in self.chat_room.users_online.all():
            self.chat_room.users_online.add(self.user)
            self.online_count()

        # self.rooms_list()

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_room_id, self.channel_name
        )

        if self.user in self.chat_room.users_online.all():
            self.chat_room.users_online.remove(self.user)
            self.online_count()
            # self.rooms_list()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        new_message = ChatMessage.objects.create(
            room=self.chat_room, user=self.user, message=message
        )

        event = {"type": "handle_message", "message_id": new_message.id}

        # self.rooms_list()
        async_to_sync(self.channel_layer.group_send)(self.chat_room_id, event)

    def handle_message(self, event):
        message_id = event["message_id"]
        message = get_object_or_404(ChatMessage, id=int(message_id))

        context = {"message": message, "user": self.user}
        html = render_to_string("chat/htmx/room_p.html", context)
        self.send(text_data=html)

    ## Online Count
    def online_count(self):
        count = self.chat_room.users_online.count()
        status = "online" if count > 1 else "offline"
        style = "background:green" if count > 1 else "background:red"
        event = {
            "type": "online_count_handler",
            "online_count": status,
            "style_status": style,
        }

        async_to_sync(self.channel_layer.group_send)(self.chat_room_id, event)

    def online_count_handler(self, event):
        count = event["online_count"]
        style = event["style_status"]
        html = render_to_string(
            "chat/htmx/online_count.html",
            {
                "online_count": count,
                "style": style,
                "room": self.chat_room,
                "user": self.user,
            },
        )

        self.send(text_data=html)

    def rooms_list(self):

        rooms = ChatRoom.objects.filter(Q(sender=self.user) | Q(receiver=self.user))
        rooms = rooms.annotate(new_message=Max("chat_message__created"))
        rooms = rooms.order_by("-new_message")

        get_last_message = ChatMessage.objects.filter(room=OuterRef("pk")).order_by(
            "-created"
        )

        rooms = rooms.annotate(
            last_message=Subquery(get_last_message.values("message")[:1]),
            created_time=Subquery(get_last_message.values("created")[:1]),
        )

        # last_message =

        event = {"type": "rooms_list_handler", "rooms": rooms}
        async_to_sync(self.channel_layer.group_send)(self.chat_room_id, event)

    def rooms_list_handler(self, event):
        rooms = event["rooms"]

        html = render_to_string(
            "chat/htmx/rooms_list.html", {"rooms": rooms, "userr": self.user}
        )
        self.send(text_data=html)
