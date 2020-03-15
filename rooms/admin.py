# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass
