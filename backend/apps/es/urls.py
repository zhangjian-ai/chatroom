from django.urls import path

from .views import *

urlpatterns = [
    path('news_search/', EsNewsSearchView.as_view()),
    path('news_suggest/', EsNewsSuggestView.as_view())
]
