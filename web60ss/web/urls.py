from django.contrib import admin
from django.urls import path, re_path, include
from .views import home_view, list_view, podcast_view
from .views import add_from_url, jump_view, search, refresh

urlpatterns = [
    path('', list_view, name='home'),
    path('list', list_view, name='list'),
    path('podcast', podcast_view, name='podcast'),
    path('jump', jump_view, name='jump'),
    path('add', add_from_url, name='add_from_url'),
    path('search', search, name='search'),
    path('refresh', refresh, name='refresh')
]