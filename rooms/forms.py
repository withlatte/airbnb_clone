from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):
    """ Search Form Definition """

    room = models.Room

    city = forms.CharField(initial="Select City")
    country = CountryField(blank_label="Select Country").formfield(required=False)
    price = forms.IntegerField(required=False)
    guest = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    room_type = forms.ModelChoiceField(
        empty_label="Select Any", queryset=models.RoomType.objects.all(), required=False
    )
    instant_book = forms.BooleanField(required=False)
    super_host = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        queryset=models.Amenity.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=models.Facility.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    # 방 사진을 업로드 하려면 로그인 사용자 ROOM 의 pk 값을 찾아
    # 그 ROOM 에 사진을 추가하기 위해 save 메쏘드에 commit False 옵션을
    # 사용하여 오버라이드 했다.
    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room

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

    def save(self, *args, **kwargs):
        room = super(CreateRoomForm, self).save(commit=False)
        return room
