from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms


class HomeView(ListView):
    """ Home View Definition """

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetailView(DetailView):
    """ Room Detail View Definition """

    model = models.Room


class SearchView(View):
    """ Search View Definition """

    def get(self, request):
        country = request.GET.get("country")
        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                beds = form.cleaned_data.get("beds")
                bedrooms = form.cleaned_data.get("bedrooms")
                baths = form.cleaned_data.get("baths")
                room_type = form.cleaned_data.get("room_type")
                instant_book = form.cleaned_data.get("instant_book")
                super_host = form.cleaned_data.get("super_host")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if super_host is True:
                    filter_args["host__super_host"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity
                for facility in facilities:
                    filter_args["facilities"] = facility
                # for amenity in amenities:
                #     filter_args["amenities"] = amenity
                #
                # for facility in facilities:
                #     filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form},)


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    """ Edit Room View Definition """

    model = models.Room
    template_name = "rooms/room_edit.html"

    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guest",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "roomtype",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    """"
    Room Photos View Definition :
    방 사진들을 나열하고 변경 및 삭제 두개의 버튼을 갖는다.
    """

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required()
def delete_photo(request, room_pk, photo_pk):
    user = request.user

    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete this photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo has been deleted successfully")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    """ Edit Photo View Definition """

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo has been edited successfully"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):
    """ Add Photo View Definition """

    model = models.Photo
    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_pk"] = self.kwargs.get("pk")

        return context

    # 너무 어렵다 진짜!
    # CreatePhotoForm 클래스에 save() 메쏘드를 오버라이드 하면서 필요한
    # pk 값을 보내기 위해 아래의  form_valid 를 오버라이드 한다고 하네.
    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo has been added successfully")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):
    """ Upload Room View Definition """

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        # Many To Many 필드데이타를 저장하기 위해서는 save_m2m() 을 사용해야하며,
        # 폼에서 commit=false 옵션사용 시, save_m2m() 사용 순서에 유의해야 한다.
        # save_m2m() 은 데이터베이스에 다른 필드들이 저장된 후에 실행되어야 한다.
        # 즉, room.save() 실행 이후, form.save_m2m() 실행
        form.save_m2m()
        messages.success(self.request, "Room has been created successfully")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
