from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST, require_safe
from django_htmx.http import reswap, retarget

from movieclub.decorators import require_auth, require_DELETE, require_form_methods
from movieclub.releases.models import Release
from movieclub.reviews.forms import ReviewForm
from movieclub.reviews.models import Review


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

        return retarget(
            reswap(
                _render_review(
                    request,
                    review,
                    {
                        "review_form": ReviewForm(),
                        "review_submit_url": request.path,
                        "new_review": True,
                    },
                ),
                "afterbegin",
            ),
            "#reviews",
        )
    return _render_review_form(request, form)


@require_safe
def review_detail(request: HttpRequest, review_id: int) -> HttpResponse:
    """Just render the review snippet."""

    review = get_object_or_404(Review, user=request.user, pk=review_id)
    return _render_review(request, review)


@require_form_methods
@require_auth
def edit_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """Update review."""
    review = get_object_or_404(Review, user=request.user, pk=review_id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated")
            return _render_review(request, review)
    else:
        form = ReviewForm(instance=review)

    return _render_review_form(request, form, {"review": review})


@require_DELETE
@require_auth
def delete_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """Delete a review."""
    review = get_object_or_404(Review, user=request.user, pk=review_id)
    review.delete()
    messages.info(request, "Your review has been deleted")
    return HttpResponse()


def _render_review(
    request: HttpRequest, review: Review, extra_context: dict | None = None
) -> HttpResponse:
    return render(
        request,
        "reviews/_review.html",
        {
            "review": review,
            **(extra_context or {}),
        },
    )


def _render_review_form(
    request: HttpRequest, form: ReviewForm, extra_context: dict | None = None
) -> HttpResponse:
    return render(
        request,
        "reviews/_review_form.html",
        {
            "review_form": form,
            "review_submit_url": request.path,
            **(extra_context or {}),
        },
    )
