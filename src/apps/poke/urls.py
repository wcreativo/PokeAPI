from django.urls import path

from .views import BerryView, HistogramImageView

urlpatterns = [
    path("allBerryStats/", BerryView.as_view(), name="allBerryStats"),
    path("getHistogram/", HistogramImageView.as_view(), name="getHistogram"),
]
