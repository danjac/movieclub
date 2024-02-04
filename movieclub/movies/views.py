from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST, require_safe
from django_htmx.http import reswap, retarget

from movieclub.client import get_client
from movieclub.decorators import require_auth
from movieclub.movies import tmdb
from movieclub.movies.forms import ReviewForm
from movieclub.movies.models import Movie


@require_safe
def index(request: HttpRequest) -> HttpResponse:
    """Returns list of movies."""
    # will paginate later
    movies = Movie.objects.order_by("-pk")[:20]
    return render(request, "movies/index.html", {"movies": movies})


@require_safe
def movie_detail(request: HttpRequest, movie_id: int, slug: str) -> HttpResponse:
    """Returns details of movie."""
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(
        request,
        "movies/movie.html",
        {
            "movie": movie,
            "reviews": movie.reviews.select_related("user").order_by("created"),
            "review_form": ReviewForm(),
        },
    )


@require_POST
@require_auth
def add_review(request: HttpRequest, movie_id: int) -> HttpResponse:
    """Create a new review for the movie."""
    movie = get_object_or_404(Movie, pk=movie_id)
    form = ReviewForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "movies/movie.html#review_form",
            {
                "movie": movie,
                "review_form": form,
            },
        )

    review = form.save(commit=False)
    review.user = request.user
    review.movie = movie
    review.save()

    messages.success(request, "Your review has been posted!")

    response = retarget(
        reswap(
            render(
                request,
                "reviews/_review.html",
                {"review": review},
            ),
            "beforeend",
        ),
        "#reviews",
    )
    response.write(
        render_to_string(
            "movies/movie.html#review_form",
            {
                "movie": movie,
                "review_form": ReviewForm(),
                "new_review": True,
            },
            request,
        )
    )
    return response


@require_safe
@transaction.non_atomic_requests
async def search_tmdb(request: HttpRequest) -> HttpResponse:
    """Search TMDB and get result.
    This should be cached!
    """
    results: list[dict] = []

    if query := request.GET.get("query", None):
        results = await tmdb.search_movies(get_client(), query)

    return render(
        request,
        "movies/_search_tmdb.html",
        {
            "search_results": results[:12],
        },
    )


@require_POST
@transaction.non_atomic_requests
@require_auth
async def add_movie(request: HttpRequest, tmdb_id: int) -> HttpResponse:
    """Given a TMDB ID, add new user and redirect there."""

    # TBD: handle 404 etc
    movie, created = await tmdb.get_or_create_movie(get_client(), tmdb_id)

    if created:
        messages.success(request, "Movie has been added")
    return redirect(movie)
