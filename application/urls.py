from django.urls import path

from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("services/",views.services,name="services"),
    path("ajax/subscribe/",views.subscribe,name="services"),
    path("ajax/send_contact_mail/",views.contact_mail,name="services"),
    path("contact/",views.contact,name="contact"),
]
