
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.views.static import serve
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path("",include("application.urls")),
    path("u/",include("user.urls")),
    path("b/",include("transactions.urls")),
    path("t/",include("tracking_system.urls")),
    path("dashboard/",include("dashboard.urls")),
    path("process1/",views.p1,name="p1"),
    path("process2/",views.process2,name="p2"),
    path("process/",views.process,name="p"),
    path("search_user/",views.search_user,name="su"),
    path("detect_cloth/",views.detect_cloth,name="dc"),
    path("complete/",views.complete_order,name="dc"),
    path("update_tracker/",views.update_tracker,name="ut"),
    path("upload_detect/",views.upload_detect,name="udc"),
    path("detect_file/",views.detect_file_url,name="udc"),
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}),

	
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)