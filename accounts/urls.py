from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "accounts"

urlpatterns = [
    path("logout/", views.logout_user, name="logout"),
]
