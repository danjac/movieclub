from django.urls import path

from movieclub.models import Release
from movieclub.releases import views

app_name = "releases"

urlpatterns = [
    path("movies/", views.movies, name="movies"),
    path(
        "movies/<slug:slug>-<int:release_id>/",
        views.release_detail,
        name="movie_detail",
        kwargs={"release_type": Release.ReleaseType.MOVIE},
    ),
    path("movies/new/<int:tmdb_id>/", views.add_movie, name="add_movie"),
    path("movies/search-tmdb/", views.search_tmdb_movies, name="search_tmdb_movies"),
    path("tv-shows/", views.tv_shows, name="tv_shows"),
    path(
        "tv-shows/<slug:slug>-<int:release_id>/",
        views.release_detail,
        name="release_detail",
        kwargs={"release_type": Release.ReleaseType.TV_SHOW},
    ),
    path("tv-shows/new/<int:tmdb_id>/", views.add_tv_show, name="add_tv_show"),
    path(
        "tv-shows/search-tmdb/", views.search_tmdb_tv_shows, name="search_tmdb_tv_shows"
    ),
    path("reviews/new/<int:release_id>/", views.add_review, name="add_review"),
    path("genre/<slug:slug>-<int:genre_id>/", views.genre_detail, name="genre_detail"),
]
