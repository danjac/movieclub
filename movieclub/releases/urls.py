from django.urls import path

from movieclub.releases import views
from movieclub.releases.models import Release

app_name = "releases"

urlpatterns = [
    path("movies/", views.movies, name="movies"),
    path(
        "movies/<slug:slug>-<int:release_id>/",
        views.release_detail,
        name="movie_detail",
        kwargs={"category": Release.Category.MOVIE},
    ),
    path("movies/new/<int:tmdb_id>/", views.add_movie, name="add_movie"),
    path("movies/search-tmdb/", views.search_tmdb_movies, name="search_tmdb_movies"),
    path("tv-shows/", views.tv_shows, name="tv_shows"),
    path(
        "tv-shows/<slug:slug>-<int:release_id>/",
        views.release_detail,
        name="tv_show_detail",
        kwargs={"category": Release.Category.TV_SHOW},
    ),
    path("tv-shows/new/<int:tmdb_id>/", views.add_tv_show, name="add_tv_show"),
    path(
        "tv-shows/search-tmdb/", views.search_tmdb_tv_shows, name="search_tmdb_tv_shows"
    ),
    path("genre/<slug:slug>-<int:genre_id>/", views.genre_detail, name="genre_detail"),
]