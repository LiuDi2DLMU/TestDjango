from django.conf.urls import url
from django.urls import include, path
from . import views


urlpatterns = [
    url("main", views.main, name="main"),
    url("index", views.index, name="index"),
    url("", views.index),
]