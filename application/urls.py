from django.urls import path,re_path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    # path("OneSignalSDKWorker.js",views.onsignal,name="os"),
    re_path(r'^OneSignalSDKWorker.js', (TemplateView.as_view(template_name="OneSignalSDKWorker.js",content_type='application/javascript')), name='OneSignalSDKWorker.js'),
    re_path(r'^sw.js', (TemplateView.as_view(template_name="sw.js",content_type='application/javascript')), name='sw.js'),
    # re_path(r'^cache-polifill.js', (TemplateView.as_view(template_name="cache-polifill.js",content_type='application/javascript')), name='cache-polifill.js'),
    re_path(r'^OneSignalSDKUpdaterWorker.js', (TemplateView.as_view(template_name="OneSignalSDKUpdaterWorker.js",content_type='application/javascript')), name='OneSignalSDKWorker.js'),
    path("about/",views.about,name="about"),
    path("test/",views.onsignal,name="test"),
    path("services/",views.services,name="services"),
    path("ajax/subscribe/",views.subscribe,name="services"),
    path("ajax/send_contact_mail/",views.contact_mail,name="services"),
    path("contact/",views.contact,name="contact"),
    path("ajax/logout/",views.logout,name="logout"),
]
