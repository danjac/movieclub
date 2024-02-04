from movieclub.movies.models import Review
from movieclub.reviews.forms import BaseReviewForm


class ReviewForm(BaseReviewForm):
    """Review form."""

    class Meta(BaseReviewForm.Meta):
        model = Review
