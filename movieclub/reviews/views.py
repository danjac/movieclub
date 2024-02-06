from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_htmx.http import reswap, retarget

from movieclub.reviews.forms import BaseReviewForm
from movieclub.reviews.models import AbstractBaseReview


def render_review_form(
    request: HttpRequest,
    form: BaseReviewForm,
    review: AbstractBaseReview | None = None,
) -> HttpResponse:
    """Renders new review and form as needed."""
    if review is not None:
        return retarget(
            reswap(
                render(
                    request,
                    "reviews/_review.html",
                    {
                        "review": review,
                        "review_form": form,
                        "review_submit_url": request.path,
                        "new_review": True,
                    },
                ),
                "afterbegin",
            ),
            "#reviews",
        )

    return render(
        request,
        "reviews/_review_form.html",
        {
            "review_form": form,
            "review_submit_url": request.path,
        },
    )
