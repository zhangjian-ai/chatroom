from django.urls import path

from .views import *

urlpatterns = [
    path('detail/', Constance.as_view()),
]
