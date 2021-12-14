from django.urls import path

from .views import *

urlpatterns = [
    path('operate/', ChatRoomView.as_view()),
]
