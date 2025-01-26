from django.urls import path

from .views import home, user_login, user_logout, user_register, chat_room_create

app_name = "accounts"

urlpatterns = [
    path("", home, name="home"),
    path("chat_room_create/", chat_room_create, name="chat_room_create"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", user_register, name="register"),
]
