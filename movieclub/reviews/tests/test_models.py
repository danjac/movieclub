from movieclub.reviews.models import Review


class TestReview:
    def test_get_score_values(self):
        review = Review(score=3)
        values = list(review.get_score_values())
        assert values == [True, True, True, False, False]
