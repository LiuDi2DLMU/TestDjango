from django.conf.urls import url
from django.urls import include, path
from . import views


urlpatterns = [
    url("main", views.main, name="main"),
    url("index", views.index, name="index"),
    url("form_submit", views.form_submit, name="form_submit"),
    url("", views.index),
]