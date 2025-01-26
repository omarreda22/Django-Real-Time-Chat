from django.urls import path

from .views import room, room_list

app_name = "chat"

urlpatterns = [
    path("room/<str:id>/", room, name="room"),
    path("list/room/", room_list, name="room_list"),
]
