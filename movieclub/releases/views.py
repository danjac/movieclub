from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_safe

from movieclub import tmdb
from movieclub.client import get_client
from movieclub.decorators import require_auth
from movieclub.pagination import render_pagination
from movieclub.releases.models import Genre, Release
from movieclub.releases.tmdb import populate_movie, populate_tv_show
from movieclub.reviews.forms import ReviewForm


@require_safe
def movies(request: HttpRequest) -> HttpResponse:
    """Returns list of movies."""
    qs = Release.objects.movies().order_by("-pk")
    search_tmdb_url = reverse("releases:search_tmdb_movies")

    if request.search:
        qs = qs.search(request.search.value)
        search_tmdb_url += "?" + request.search.qs

    return render_pagination(
        request,
        movies,
        "releases/movies.html",
        {
            "search_tmdb_url": search_tmdb_url,
        },
    )


@require_safe
def tv_shows(request: HttpRequest) -> HttpResponse:
    """Returns list of TV shows."""
    qs = Release.objects.movies().order_by("-pk")
    search_tmdb_url = reverse("releases:search_tmdb_tv_shows")

    if request.search:
        qs = qs.search(request.search.value)
        search_tmdb_url += "?" + request.search.qs

    return render_pagination(
        request,
        qs,
        "releases/tv_shows.html",
        {
            "search_tmdb_url": search_tmdb_url,
        },
    )


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
        "movies/genre.html",
        {
            "genre": genre,
        },
    )


@require_safe
def release_detail(
    request: HttpRequest,
    release_type: Release.ReleaseType,
    release_id: int,
    slug: str,
) -> HttpResponse:
    """Returns details of movie."""
    release = get_object_or_404(release_type=release_type, pk=release_id)
    context = {
        "movie": release,
        "reviews": release.reviews.select_related("user").order_by("-created"),
        "cast_members": release.cast_members.select_related("person").order_by("order"),
        "crew_members": release.crew_members.select_related("person"),
    }
    if request.user.is_authenticated:
        context = {
            **context,
            "review_form": ReviewForm(),
            "review_submit_url": reverse(
                "releases:add_review",
                kwargs={"release_id": release.pk},
            ),
        }

    return render(request, "releases/release.html", context)


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
    results: list[tmdb.Movie] = []

    if request.search:
        results = tmdb.search_movies(get_client(), request.search)

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
    results: list[tmdb.TVShow] = []

    if request.search:
        results = tmdb.search_tv_shows(get_client(), request.search)

    return render(
        request,
        "releases/search_tmdb_tv_shows.html",
        {
            "search_results": results[:limit],
        },
    )
