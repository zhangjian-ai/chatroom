from django.urls import path

from .views import *

urlpatterns = [
    path('news_search/', EsNewsSearch.as_view()),
]
