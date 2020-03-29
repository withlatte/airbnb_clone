# Function Based View(fbv) Coding instead Class Based View(cbv>

# from math import ceil
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from . import models as room_models


def show_rooms(request):
    page = request.GET.get("page", 1)
    room_list = room_models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/room_list.html", {"rooms": rooms})
    except (EmptyPage, ValueError):
        return redirect("/")

    # page = request.GET.get("page", default=1)
    # page = int(page or 1)
    # page_size = 10
    # limit = page_size * page
    # offset = limit - page_size
    #
    # room_model = room_models.Room.objects.all()[offset:limit]
    # count_page = ceil(room_models.Room.objects.count() / page_size)
    #
    # return render(
    #     request,
    #     "rooms/room_list.html",
    #     context={
    #         "room_model": room_model,
    #         "page": page,
    #         "count_page": count_page,
    #         "page_range": range(1, count_page + 1),
    #     },
    # )
