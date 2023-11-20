from django.urls import path

from .views import BerryView

urlpatterns = [path("", BerryView.as_view(), name="berries")]
