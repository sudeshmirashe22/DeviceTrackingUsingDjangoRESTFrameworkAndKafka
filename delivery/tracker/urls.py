# tracker/urls.py
from django.urls import path
from .views import LocationUpdateAPI
from tracker.views import *

urlpatterns = [
    path("", index),
    path("data/", get_data),
    path('track/', LocationUpdateAPI.as_view()),
    path('hello/', hello)
]
