import http

import pytest
from django.urls import reverse

from movieclub.releases.tests.factories import create_movie
from movieclub.reviews.models import Review
from movieclub.reviews.tests.factories import create_review
from movieclub.tests.factories import create_batch


@pytest.fixture()
def review(auth_user):
    return create_review(user=auth_user)


@pytest.fixture()
def movie():
    return create_movie()


class TestReleaseReviewList:
    @pytest.fixture()
    def url(self, movie):
        return reverse("reviews:release_review_list", args=[movie.pk])

    @pytest.mark.django_db()
    def test_get(self, client, movie, url):
        create_batch(create_review, 3, release=movie)

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK


class TestUserReviewList:
    @pytest.fixture()
    def url(self, user):
        return reverse("reviews:user_review_list", args=[user.username])

    @pytest.mark.django_db()
    def test_get(self, client, user, url):
        create_batch(create_review, 3, user=user)

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK


class TestReviewDetail:
    @pytest.mark.django_db()
    def test_get(self, client, review):
        response = client.get(review.get_absolute_url())

        assert response.status_code == http.HTTPStatus.OK


class TestAddReview:
    @pytest.fixture()
    def url(self, movie):
        return reverse("reviews:add_review", args=[movie.pk])

    @pytest.mark.django_db()
    def test_post(self, client, auth_user, movie, url):
        response = client.post(
            url,
            {"comment": "test", "score": 3},
        )
        review = Review.objects.get()
        assert response.url == review.get_absolute_url()
        assert review.release == movie
        assert review.user == auth_user

    @pytest.mark.django_db()
    def test_get(self, client, auth_user, url):
        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_review_exists(self, client, auth_user, movie, url):
        create_review(user=auth_user, release=movie)
        response = client.get(url)

        assert response.status_code == http.HTTPStatus.FORBIDDEN


class TestEditReview:
    @pytest.fixture()
    def url(self, review):
        return reverse("reviews:edit_review", args=[review.pk])

    @pytest.mark.django_db()
    def test_get(self, client, review, url):
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post(self, client, review, url):
        response = client.post(
            url,
            {
                "comment": "test",
                "score": 3,
            },
        )
        assert response.url == review.get_absolute_url()
        review.refresh_from_db()
        assert review.comment == "test"


class TestDeleteReview:
    @pytest.mark.django_db()
    def test_delete(self, client, review):
        response = client.delete(
            reverse("reviews:delete_review", args=[review.pk]),
        )
        assert response.url == review.release.get_absolute_url()
        assert Review.objects.count() == 0
