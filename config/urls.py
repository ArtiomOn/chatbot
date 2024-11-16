from django.contrib import admin
from django.urls import path

from apps.chat.views import chat_view, reset_chat

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", chat_view, name="chat"),
    path("reset-chat/", reset_chat, name="reset_chat"),
]
