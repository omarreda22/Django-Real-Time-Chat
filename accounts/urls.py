from django.urls import path

from .views import home, user_login

app_name = "accounts"

urlpatterns = [
    path("", home, name="home"),
    path("login/", user_login, name="login"),
]
