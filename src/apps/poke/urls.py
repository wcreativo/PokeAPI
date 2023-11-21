from django.urls import path

from .views import BerryView

urlpatterns = [path("allBerryStats/", BerryView.as_view(), name="allBerryStats")]
