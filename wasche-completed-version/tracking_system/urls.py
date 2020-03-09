
from django.contrib import admin
from django.urls import path,include,re_path
from .views import render_track
urlpatterns = [
    path("",render_track,name="render_track"),

]