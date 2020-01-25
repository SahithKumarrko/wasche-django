
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.views.static import serve

from django.conf.urls.static import static
urlpatterns = [
    path("",include("application.urls")),
    path("u/",include("user.urls")),
    path("b/",include("transactions.urls")),
    path("dashboard/",include("dashboard.urls")),
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)