from django.urls import path
from . import views



urlpatterns = [
    path('', views.index),
    path('sign_in', views.sign_in),
    path('callback', views.callback),
    path('genreresult', views.genre_result),
    path('genremoods', views.genremoods),
    path('new_releases', views.new_releases),
    path('chart', views.charts),
    path('concert', views.concerts),
    path('search_track', views.search_track),
    path('track_results', views.track_results),
    path('get_playlists', views.get_playlists),
    path('new_playlist', views.new_playlist),
    path('create_playlist', views.create_playlist),
    path('add_song_to_playlist/<str:track_id>', views.add_song_to_playlist),
    path('new_song_in_playlist', views.new_song_in_playlist),
]
