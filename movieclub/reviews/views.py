from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from movieclub.reviews.forms import BaseReviewForm
from movieclub.reviews.models import BaseReview


def render_review(
    request: HttpRequest,
    review: BaseReview,
    extra_context: dict | None = None,
) -> HttpResponse:
    """Render a review snippet."""
    return render(
        request,
        "reviews/_review.html",
        {
            "review": review,
            **(extra_context or {}),
        },
    )


def render_review_form(
    request: HttpRequest,
    form: BaseReviewForm,
    review: BaseReview | None = None,
    extra_context: dict | None = None,
):
    """Renders review form."""
    return render(
        request,
        "reviews/_review_form.html",
        {
            "review": review,
            "review_form": form,
            "review_submit_url": request.path,
            **(extra_context or {}),
        },
    )
