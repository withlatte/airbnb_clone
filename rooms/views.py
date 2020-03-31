from django.views.generic import ListView
from django.shortcuts import render
from django.http import Http404
from . import models


class HomeView(ListView):
    """ Home View Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404


def search(request):
    city = request.GET.get("city")
    city = str.capitalize(city)
    return render(request, "rooms/search.html", {"city": city})


""" 
>> Using Class Room Detail
    (rooms/url.py) urlpatterns = [path("<int:pk>", views.RoomDetail.as_view(), name="detail")]

    from django.views.generic import DetailView

    class RoomDetail(Detail.View):
        model = models.Room
"""
