from django.urls import path,re_path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    # path("gone-offline.html/",views.offline,name="offline"),
    re_path(r'^gone-offline.html', (TemplateView.as_view(template_name="offline.html",content_type='text/html')), name='offline'),

    # path("OneSignalSDKWorker.js",views.onsignal,name="os"),
    re_path(r'^OneSignalSDKWorker.js', (TemplateView.as_view(template_name="OneSignalSDKWorker.js",content_type='application/javascript')), name='OneSignalSDKWorker.js'),
    re_path(r'^sw.js', (TemplateView.as_view(template_name="sw.js",content_type='application/javascript')), name='sw.js'),
    # re_path(r'^cache-polifill.js', (TemplateView.as_view(template_name="cache-polifill.js",content_type='application/javascript')), name='cache-polifill.js'),
    re_path(r'^OneSignalSDKUpdaterWorker.js', (TemplateView.as_view(template_name="OneSignalSDKUpdaterWorker.js",content_type='application/javascript')), name='OneSignalSDKWorker.js'),
    path("about/",views.about,name="about"),
    path("test/",views.onsignal,name="test"),
    path("update_notification/",views.update_notification_setting,name="test"),
    path("services/",views.services,name="services"),
    path("ajax/subscribe/",views.subscribe,name="subscribe"),
    path("ajax/get_notification/",views.get_notifications,name="get_notifications"),
    path("ajax/update_user_notification_set/",views.update_notifications,name="update_notifications"),
    path("ajax/get_new_notification/",views.get_new_notifications,name="get_new_notifications"),
    path("ajax/send_contact_mail/",views.contact_mail,name="contact_mail"),
    path("contact/",views.contact,name="contact"),
    path("ajax/logout/",views.logout,name="logout"),
    path("api/notify_initial/",views.notify_user,name="notify_user"),
]
