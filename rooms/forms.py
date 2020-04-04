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
