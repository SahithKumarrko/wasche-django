from django.urls import path

from . import views
urlpatterns = [
    path("",views.user_contract_page,name="user_contract_page"),
]