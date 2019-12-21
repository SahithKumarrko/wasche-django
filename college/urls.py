from django.urls import path

from . import views
urlpatterns = [
    path("",views.user_collge_page,name="user_college_page"),
]