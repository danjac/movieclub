from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_safe

from movieclub.decorators import require_auth, require_DELETE, require_form_methods
from movieclub.htmx import render_htmx
from movieclub.pagination import render_pagination
from movieclub.releases.models import Release
from movieclub.reviews.forms import ReviewForm
from movieclub.reviews.models import Review
from movieclub.users.models import User


@require_safe
def release_review_list(
    request: HttpRequest, release_id: int, slug: str
) -> HttpResponse:
    """List of reviews for a release."""

    release = get_object_or_404(Release, pk=release_id)

    return render_pagination(
        request,
        "reviews/release_list.html",
        release.reviews.select_related("release", "user").order_by("-created"),
        {
            "release": release,
        },
    )


@require_safe
def user_review_list(request: HttpRequest, username: str) -> HttpResponse:
    """List of reviews published by a user."""

    user = get_object_or_404(User, is_active=True, username__iexact=username)

    return render_pagination(
        request,
        "reviews/user_list.html",
        user.reviews.select_related("release", "user").order_by("-created"),
        {
            "reviewer": user,
        },
    )


@require_safe
def review_detail(request: HttpRequest, review_id: int) -> HttpResponse:
    """Review detail."""
    review = get_object_or_404(
        Review.objects.select_related("release", "user"), pk=review_id
    )
    return render(request, "reviews/detail.html", {"review": review})


@require_POST
@require_auth
def add_review(request: HttpRequest, release_id: int) -> HttpResponse:
    """Add new review"""
    release = get_object_or_404(Release, pk=release_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.release = release
        review.save()

        messages.success(request, "Your review has been posted, thanks!")
        return redirect(review)

    return _render_review_form(request, form)


@require_form_methods
@require_auth
def edit_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """Update review."""
    review = get_object_or_404(
        Review.objects.select_related("release", "user"),
        user=request.user,
        pk=review_id,
    )

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated")
            return redirect(review)

    else:
        form = ReviewForm(instance=review)

    return _render_review_form(request, form, {"review": review})


@require_DELETE
@require_auth
def delete_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """Delete a review."""
    review = get_object_or_404(
        Review.objects.select_related("release"),
        user=request.user,
        pk=review_id,
    )
    review.delete()
    messages.info(request, "Your review has been deleted")

    return redirect("reviews:user_review_list", args=[request.user.username])


def _render_review_form(
    request: HttpRequest, form: ReviewForm, extra_context: dict | None = None
) -> HttpResponse:
    return render_htmx(
        request,
        "reviews/review_form.html",
        {"form": form} | (extra_context or {}),
        partial="form",
        target="review-form",
    )
