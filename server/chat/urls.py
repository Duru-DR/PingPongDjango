from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('user/', DataView.as_view()),
    path('messages/history/', LoadMessagesView.as_view()),
    path('chats/', ChatsView.as_view()),
]
