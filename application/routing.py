from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<room_name>\w+)/$', consumers.Consumer),
    # re_path(r'ws/(?P<room_name>([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,8}))/$', consumers.Consumer),
    re_path(r'wss/(?P<room_name>\w+)/$', consumers.Consumer),
]