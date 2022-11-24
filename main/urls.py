from django.conf.urls import url
from django.urls import include, path
from . import views


urlpatterns = [
    url("zsm/", views.zsm, name="zsm"),
    url("neuropeptide/", views.neuropepetide, name="neuropeptide"),
    url("index", views.index, name="index"),
    url("", views.index),
]
