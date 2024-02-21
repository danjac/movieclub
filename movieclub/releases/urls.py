from django.urls import path

from movieclub.releases import views

app_name = "releases"

urlpatterns = [
    path("movies/", views.movie_list, name="movie_list"),
    path(
        "movies/<slug:slug>-<int:release_id>/",
        views.movie_detail,
        name="movie_detail",
    ),
    path(
        "movies/new/<int:tmdb_id>/",
        views.add_movie,
        name="add_movie",
    ),
    path(
        "movies/search-tmdb/",
        views.search_tmdb_movies,
        name="search_tmdb_movies",
    ),
    path("tv-shows/", views.tv_show_list, name="tv_show_list"),
    path(
        "tv-shows/<slug:slug>-<int:release_id>/",
        views.tv_show_detail,
        name="tv_show_detail",
    ),
    path(
        "tv-shows/new/<int:tmdb_id>/",
        views.add_tv_show,
        name="add_tv_show",
    ),
    path(
        "tv-shows/search-tmdb/",
        views.search_tmdb_tv_shows,
        name="search_tmdb_tv_shows",
    ),
    path(
        "genre/<slug:slug>-<int:genre_id>/",
        views.genre_detail,
        name="genre_detail",
    ),
]
