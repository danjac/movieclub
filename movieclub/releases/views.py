from typing import TYPE_CHECKING

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_safe

from movieclub.client import get_client
from movieclub.decorators import require_auth
from movieclub.pagination import render_pagination
from movieclub.releases.models import Genre, Release, ReleaseQuerySet
from movieclub.tmdb import populate_movie, populate_tv_show
from movieclub.tmdb.api import search_movies, search_tv_shows

if TYPE_CHECKING:  # pragma: no cover
    from movieclub.tmdb.models import Movie, TVShow


@require_safe
def movie_list(request: HttpRequest) -> HttpResponse:
    """Returns list of movies."""
    return _render_release_list(
        request,
        Release.objects.movies(),
        "releases/movies.html",
        search_tmdb_url=reverse("releases:search_tmdb_movies"),
    )


@require_safe
def movie_detail(request: HttpRequest, release_id: int, slug: str) -> HttpResponse:
    """Render TV show details."""
    return _render_release_detail(request, release_id, Release.objects.movies())


@require_safe
def tv_show_list(request: HttpRequest) -> HttpResponse:
    """Returns list of TV shows."""
    return _render_release_list(
        request,
        Release.objects.tv_shows(),
        "releases/tv_shows.html",
        search_tmdb_url=reverse("releases:search_tmdb_tv_shows"),
    )


@require_safe
def tv_show_detail(request: HttpRequest, release_id: int, slug: str) -> HttpResponse:
    """Render TV show details."""
    return _render_release_detail(request, release_id, Release.objects.tv_shows())


@require_safe
def genre_detail(request: HttpRequest, genre_id: int, slug: str) -> HttpResponse:
    """Returns list of movies for a genre."""

    genre = get_object_or_404(Genre, pk=genre_id)
    releases = genre.movies.order_by("-release_date")

    if request.search:
        releases = releases.search(request.search.value)

    return render_pagination(
        request,
        releases,
        "releases/genre.html",
        {
            "genre": genre,
        },
    )


@require_POST
@require_auth
def add_movie(request: HttpRequest, tmdb_id: int) -> HttpResponse:
    """Given a TMDB ID, add new user and redirect there."""

    try:
        movie = Release.objects.movies().get(tmdb_id=tmdb_id)
    except Release.DoesNotExist:
        movie = populate_movie(get_client(), tmdb_id)
        messages.success(request, "Movie has been added")

    return redirect(movie)


@require_POST
@require_auth
def add_tv_show(request: HttpRequest, tmdb_id: int) -> HttpResponse:
    """Given a TMDB ID, add new user and redirect there."""

    try:
        tv_show = Release.objects.tv_shows().get(tmdb_id=tmdb_id)
    except Release.DoesNotExist:
        tv_show = populate_tv_show(get_client(), tmdb_id)
        messages.success(request, "TV show has been added")

    return redirect(tv_show)


@require_safe
@require_auth
def search_tmdb_movies(request: HttpRequest, limit: int = 12) -> HttpResponse:
    """Search TMDB and get result.

    TBD: make full page, with "Add" button.
    """
    results: list[Movie] = []

    if request.search:
        results = search_movies(get_client(), request.search)

    return render(
        request,
        "releases/search_tmdb_movies.html",
        {
            "search_results": results[:limit],
        },
    )


@require_safe
@require_auth
def search_tmdb_tv_shows(request: HttpRequest, limit: int = 12) -> HttpResponse:
    """Search TMDB and get result.

    TBD: make full page, with "Add" button.
    """
    results: list[TVShow] = []

    if request.search:
        results = search_tv_shows(get_client(), request.search)

    return render(
        request,
        "releases/search_tmdb_tv_shows.html",
        {
            "search_results": results[:limit],
        },
    )


def _render_release_list(
    request: HttpRequest,
    releases: ReleaseQuerySet,
    template_name: str,
    *,
    search_tmdb_url: str,
) -> HttpResponse:
    if request.search:
        releases = releases.search(request.search.value).order_by("-rank")
        search_tmdb_url += "?" + request.search.qs
    else:
        releases = releases.order_by("-release_date")

    return render_pagination(
        request,
        releases,
        template_name,
        {
            "search_tmdb_url": search_tmdb_url,
        },
    )


def _render_release_detail(
    request: HttpRequest, release_id: int, queryset: ReleaseQuerySet
) -> HttpResponse:
    release = get_object_or_404(queryset, pk=release_id)
    context = {
        "release": release,
        "cast_members": release.cast_members.select_related("person").order_by("order"),
        "crew_members": release.crew_members.select_related("person"),
    }
    return render(request, "releases/release.html", context)
