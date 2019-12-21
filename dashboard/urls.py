from django.urls import path

from dashboard import views
urlpatterns = [
    path("",views.open_dashboard_page,name="dashboard"),
]
