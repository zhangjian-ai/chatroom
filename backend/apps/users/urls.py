from django.urls import path

from .views import *

urlpatterns = [
    path('logon/', LogonView.as_view()),
    path('login/', LoginView.as_view()),
]
