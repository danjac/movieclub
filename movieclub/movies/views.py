from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_safe
from django_htmx.http import reswap, retarget

from movieclub import tmdb
from movieclub.client import get_client
from movieclub.decorators import require_auth, require_DELETE, require_form_methods
from movieclub.movies.forms import ReviewForm
from movieclub.movies.models import Movie, Review
from movieclub.movies.tmdb import populate_movie
from movieclub.pagination import render_pagination
from movieclub.reviews.views import render_review, render_review_form


@require_safe
def index(request: HttpRequest) -> HttpResponse:
    """Returns list of movies."""
    movies = Movie.objects.order_by("-pk")
    search_tmdb_url = reverse("movies:search_tmdb")

    if request.search:
        movies = movies.filter(
            Q(title__icontains=request.search.value)
            | Q(cast_members__person__name__icontains=request.search.value)
            | Q(crew_members__person__name__icontains=request.search.value)
        ).distinct()
        search_tmdb_url += "?" + request.search.qs

    return render_pagination(
        request,
        movies,
        "movies/index.html",
        {
            "search_tmdb_url": search_tmdb_url,
        },
    )


@require_safe
def movie_detail(request: HttpRequest, movie_id: int, slug: str) -> HttpResponse:
    """Returns details of movie."""
    movie = get_object_or_404(Movie, pk=movie_id)
    context = {
        "movie": movie,
        "reviews": movie.reviews.select_related("user").order_by("-created"),
        "cast_members": movie.cast_members.exclude(person__profile_url="")
        .select_related("person")
        .order_by("order")[:6],
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
@require_auth
def search_tmdb(request: HttpRequest, limit: int = 12) -> HttpResponse:
    """Search TMDB and get result.

    TBD: make full page, with "Add" button.
    """
    results: list[tmdb.Movie] = []

    if request.search:
        results = tmdb.search_movies(get_client(), request.search)

    return render(
        request,
        "movies/search_tmdb.html",
        {
            "search_results": results[:limit],
        },
    )


@require_POST
@require_auth
def add_movie(request: HttpRequest, tmdb_id: int) -> HttpResponse:
    """Given a TMDB ID, add new user and redirect there."""

    try:
        movie = Movie.objects.get(tmdb_id=tmdb_id)
    except Movie.DoesNotExist:
        movie = populate_movie(get_client(), tmdb_id)
        messages.success(request, "Movie has been added")

    return redirect(movie)
