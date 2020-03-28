from django.shortcuts import render
from . import models as room_models


# Create your views here.
def show_rooms(request):
    room_model = room_models.Room.objects.all()
    return render(request, "rooms/home.html", context={"room_model": room_model},)
