from django.urls import path

from movieclub.movies import views

app_name = "movies"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/<int:tmdb_id>/", views.add_movie, name="add_movie"),
    path("search-tmdb/", views.search_tmdb, name="search_tmdb"),
    path("reviews/new/<int:movie_id>/", views.add_review, name="add_review"),
    path("reviews/<int:review_id>/delete", views.delete_review, name="delete_review"),
    path("<slug:slug>-<int:movie_id>/", views.movie_detail, name="movie_detail"),
]
