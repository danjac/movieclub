from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_htmx.http import reswap, retarget

from movieclub.reviews.forms import BaseReviewForm
from movieclub.reviews.models import AbstractBaseReview


def render_new_review(
    request: HttpRequest,
    review: AbstractBaseReview,
    form: BaseReviewForm,
    *,
    hx_retarget: str | None = "#reviews",
    hx_reswap="afterbegin",
    extra_context: dict | None = None,
) -> HttpResponse:
    """Render new review after successful submit."""
    return render_review(
        request,
        review,
        hx_retarget=hx_retarget,
        hx_reswap=hx_reswap,
        extra_context={
            "review_form": form,
            "review_submit_url": request.path,
            "new_review": True,
            **(extra_context or {}),
        },
    )


def render_updated_review(
    request: HttpRequest,
    review: AbstractBaseReview,
    *,
    hx_retarget: str | None = None,
    hx_reswap="innerHTML",
    **kwargs,
):
    """Render review after successful update."""
    return render_review(
        request,
        review,
        hx_retarget=hx_retarget or f"#{review.get_target_id()}",
        hx_reswap=hx_reswap,
    )


def render_review_form(
    request: HttpRequest,
    form: BaseReviewForm,
    review: AbstractBaseReview | None = None,
    extra_context: dict | None = None,
) -> HttpResponse:
    """Renders review form."""
    return render(
        request,
        "reviews/_review_form.html",
        {
            **(extra_context or {}),
            "review": review,
            "review_form": form,
            "review_submit_url": request.path,
        },
    )


def render_review(
    request: HttpRequest,
    review: AbstractBaseReview,
    *,
    hx_reswap=None,
    hx_retarget: str | None = None,
    extra_context: dict | None = None,
) -> HttpResponse:
    """Renders review snippet."""

    response = render(
        request,
        "reviews/_review.html",
        {
            "review": review,
            **(extra_context or {}),
        },
    )

    if hx_reswap:
        response = reswap(response, hx_reswap)
    if hx_retarget:
        response = retarget(response, hx_retarget)

    return response
