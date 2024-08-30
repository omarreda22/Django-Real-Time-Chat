from django.urls import path

from .views import room

app_name = "chat"

urlpatterns = [
    path("room/<str:id>/", room, name="room"),
]
