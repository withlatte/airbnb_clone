from django.urls import path
from rooms import views as room_views

# Create your views here.
app_name = "core"

urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]
