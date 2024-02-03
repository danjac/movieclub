from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_safe

from movieclub.client import get_client
from movieclub.decorators import arequire_auth
from movieclub.movies import tmdb
from movieclub.movies.models import Movie


@require_safe
def movie_detail(request: HttpRequest, movie_id: int) -> HttpResponse:
    """Returns details of movie."""
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, "movies/movie.html", {"movie": movie})


@require_safe
async def search_tmdb(request: HttpRequest) -> HttpResponse:
    """Search TMDB and get result.
    This should be cached!
    """
    results: list[dict] = []

    if query := request.GET.get("query", None):
        results = await tmdb.search_movies(get_client(), query)

    return render(request, "movies/search_tmdb.html", {"search_results": results})


@require_POST
@arequire_auth
async def add_movie_from_tmdb(request: HttpRequest, tmdb_id: int) -> HttpResponse:
    """Given a TMDB ID, add new user and redirect there."""

    # TBD: handle 404 etc
    movie, created = await tmdb.get_or_create_movie(get_client(), tmdb_id)

    if created:
        messages.success(request, "Movie has been added")
    return redirect(movie)
