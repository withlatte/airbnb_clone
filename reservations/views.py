import datetime
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.http import Http404
from rooms import models as room_models
from django.contrib import messages
from reviews import forms as review_forms
from . import models


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room_obj = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room_obj)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't make reservation on this room")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room_obj = room_models.Room.objects.get(pk=room)
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room_obj,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )

        if reservation.pk is not None:
            return redirect(
                reverse("reservations:detail", kwargs={"pk": reservation.pk})
            )
        else:
            messages.error(request, "Can't make reservation on this room")
            return redirect(reverse("rooms:detail", kwargs={"pk": reservation.room.pk}))


class ReservationDetailView(View):
    """ Reservation Detail View Definition """

    def get(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        # models.MYCLASS.objects 를 model manager 라고하며, managers.py 를 통해 오버라이드 가능하다.
        #  get_object_or_404 method 를 사용하는 것도 get_on_none 과 동일한 기능을 구현한다.
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = review_forms.CreateReviewForm()
        return render(
            request=self.request,
            template_name="reservations/detail.html",
            context={"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)

    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirmed":
        reservation.status = models.Reservation.STATUS_CONFIRMED
        reservation.save()
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
    elif verb == "canceled":
        reservation.delete()
        messages.success(request, f"Your reservation has been canceled")
        return redirect(reverse("rooms:detail", kwargs={"pk": reservation.room.pk}))

    messages.success(request, f"Your reservation has been {verb}")
