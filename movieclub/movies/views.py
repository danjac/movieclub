from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_safe
from django_htmx.http import reswap, retarget

from movieclub.client import get_client
from movieclub.decorators import require_auth, require_DELETE, require_form_methods
from movieclub.movies import tmdb
from movieclub.movies.forms import ReviewForm
from movieclub.movies.models import Movie, Review
from movieclub.reviews.views import render_review, render_review_form


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
    context = {
        "movie": movie,
        "reviews": movie.reviews.select_related("user").order_by("-created"),
        "cast_members": movie.cast_members.select_related("person").order_by("order")[
            :6
        ],
    }
    if request.user.is_authenticated:
        context = {
            **context,
            "review_form": ReviewForm(),
            "review_submit_url": reverse(
                "movies:add_review",
                kwargs={"movie_id": movie.pk},
            ),
        }

    return render(request, "movies/movie.html", context)


@require_POST
@require_auth
def add_review(request: HttpRequest, movie_id: int) -> HttpResponse:
    """Create a new review for the movie."""
    movie = get_object_or_404(Movie, pk=movie_id)

    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.movie = movie
        review.save()

        messages.success(request, "Your review has been posted!")

        return retarget(
            reswap(
                render_review(
                    request,
                    review,
                    {
                        "new_review": True,
                        "review_submit_url": request.path,
                        "review_form": ReviewForm(),
                    },
                ),
                "afterbegin",
            ),
            "#reviews",
        )

    return render_review_form(request, form)


@require_form_methods
@require_auth
def edit_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """Edit review."""
    review = get_object_or_404(
        Review.objects.select_related("user"),
        user=request.user,
        pk=review_id,
    )

    if request.GET.get("action") == "cancel":
        return render_review(request, review)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated")
            return retarget(
                reswap(
                    render_review(request, review),
                    "innerHTML",
                ),
                f"#{review.get_target_id()}",
            )
    else:
        form = ReviewForm(instance=review)

    return render_review_form(request, form, review)


@require_DELETE
@require_auth
def delete_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """Delete a review"""
    Review.objects.filter(user=request.user, pk=review_id).delete()
    messages.info(request, "Your review has been deleted")
    return HttpResponse()


@require_safe
@transaction.non_atomic_requests
# TBD: should be auth only
async def search_tmdb(request: HttpRequest, limit: int = 12) -> HttpResponse:
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
            "search_results": results[:limit],
        },
    )


@require_POST
@require_auth
@transaction.non_atomic_requests
async def add_movie(request: HttpRequest, tmdb_id: int) -> HttpResponse:
    """Given a TMDB ID, add new user and redirect there."""

    # TBD: handle 404 etc
    movie, created = await tmdb.get_or_create_movie(get_client(), tmdb_id)

    if created:
        messages.success(request, "Movie has been added")
    return redirect(movie)
