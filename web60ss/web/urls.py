from django.contrib import admin
from django.urls import path, re_path, include
from .views import home_view, list_view, podcast_view
from .views import read_data_from_json, add_from_url, jump_view

urlpatterns = [
    path('', list_view, name='home'),
    # path('list', list_view, name='list'),
    path('podcast', podcast_view, name='podcast'),
    path('jump', jump_view, name='jump'),
    path('add', add_from_url, name='add_from_url'),
    path('read_data_from_json', read_data_from_json),
]