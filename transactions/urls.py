
from django.urls import path
from . import views
urlpatterns = [
    path("start/",views.start_transaction,name="start"),
    path("check_status/",views.check_transaction,name="start"),
    
]
