from django.contrib import admin
from django.urls import path

from apps.chat.views import chat_view, reset_chat, stream_response

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", chat_view, name="chat"),
    path("stream-response/", stream_response, name="stream_response"),
    path("reset-chat/", reset_chat, name="reset_chat"),
]
