from django.urls import path

from .views import *

urlpatterns = [
    path('search/', LogonView.as_view()),
]
