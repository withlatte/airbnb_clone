from django.urls import path
from django.shortcuts import render
from rooms import views as room_views

# Create your views here.
app_name = "core"

urlpatterns = [path("", room_views.show_rooms, name="home")]
