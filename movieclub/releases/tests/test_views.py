import http

import pytest
from django.urls import reverse, reverse_lazy

from movieclub import tmdb
from movieclub.movies.models import Movie, Review
from movieclub.movies.tests.factories import create_genre, create_movie, create_review
from movieclub.tests.factories import create_batch


class TestIndex:
    url = reverse_lazy("movies:index")

    @pytest.mark.django_db()
    def test_get(self, client):
        create_batch(create_movie, 10)
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_search(self, client):
        movie = create_movie(title="Jaws")
        response = client.get(self.url, {"query": "jaws"})
        assert response.status_code == http.HTTPStatus.OK
        assert movie in response.context["page_obj"].object_list


class TestGenreDetail:
    @pytest.fixture()
    def genre(self):
        return create_genre()

    @pytest.mark.django_db()
    def test_get(self, client, genre):
        for movie in create_batch(create_movie, 10):
            genre.movies.add(movie)
        response = client.get(genre.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_search(self, client, genre):
        movie = create_movie(title="Jaws")
        genre.movies.add(movie)
        response = client.get(genre.get_absolute_url(), {"query": "jaws"})
        assert response.status_code == http.HTTPStatus.OK
        assert movie in response.context["page_obj"].object_list


class TestDetail:
    @pytest.mark.django_db()
    def test_get(self, client):
        movie = create_movie()
        create_batch(create_review, 3, movie=movie)
        response = client.get(movie.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_for_user(self, client, auth_user):
        movie = create_movie()
        create_batch(create_review, 3, movie=movie)
        response = client.get(movie.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK


class TestAddReview:
    @pytest.mark.django_db()
    def test_post(self, client, auth_user):
        movie = create_movie()
        response = client.post(
            reverse("movies:add_review", args=[movie.pk]),
            {"comment": "test!"},
        )

        assert response.status_code == http.HTTPStatus.OK
        assert movie.reviews.filter(user=auth_user).count() == 1

    @pytest.mark.django_db()
    def test_post_invalid(self, client, auth_user):
        movie = create_movie()
        response = client.post(reverse("movies:add_review", args=[movie.pk]), {})

        assert response.status_code == http.HTTPStatus.OK
        assert movie.reviews.filter(user=auth_user).count() == 0


class TestEditReview:
    @pytest.mark.django_db()
    def test_get_is_owner(self, client, auth_user):
        review = create_review(user=auth_user)
        response = client.get(review.get_edit_url())
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_cancel(self, client, auth_user):
        review = create_review(user=auth_user)
        response = client.get(review.get_edit_url(), {"action": "cancel"})
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_is_not_owner(self, client, auth_user):
        review = create_review()
        response = client.get(review.get_edit_url())
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.django_db()
    def test_post(self, client, auth_user):
        review = create_review(user=auth_user)
        response = client.post(
            review.get_edit_url(),
            {
                "comment": "updated comment!",
                "url": "https://example.com",
            },
        )
        assert response.status_code == http.HTTPStatus.OK

        review.refresh_from_db()
        assert review.comment == "updated comment!"
        assert review.url == "https://example.com"


class TestDeleteReview:
    @pytest.mark.django_db()
    def test_delete_is_owner(self, client, auth_user):
        review = create_review(user=auth_user)
        response = client.delete(review.get_delete_url())
        assert response.status_code == http.HTTPStatus.OK
        assert Review.objects.exists() is False

    @pytest.mark.django_db()
    def test_delete_is_not_owner(self, client, auth_user):
        review = create_review()
        response = client.delete(review.get_delete_url())
        assert response.status_code == http.HTTPStatus.OK
        assert Review.objects.exists() is True


class TestSearchTmdb:
    url = reverse_lazy("movies:search_tmdb")

    @pytest.mark.django_db()
    def test_get(self, client, mocker, auth_user):
        mocker.patch(
            "movieclub.tmdb.search_movies",
            return_value=[
                tmdb.Movie(
                    id=1000,
                    title="John Wick",
                    release_date="2014-01-01",
                )
            ],
        )

        response = client.get(self.url, {"query": "Wick"})
        assert response.status_code == http.HTTPStatus.OK


class TestAddMovie:
    tmdb_id = 245891
    url = reverse_lazy("movies:add_movie", args=[tmdb_id])

    @pytest.mark.django_db()
    def test_post_new(self, client, auth_user, mocker):
        movie = create_movie(tmdb_id=self.tmdb_id)

        mocker.patch(
            "movieclub.movies.models.Movie.objects.get",
            side_effect=Movie.DoesNotExist,
        )

        mocker.patch(
            "movieclub.movies.views.populate_movie",
            return_value=movie,
        )

        response = client.post(self.url)
        assert response.url == movie.get_absolute_url()

    @pytest.mark.django_db()
    def test_post_exists(self, client, auth_user):
        movie = create_movie(tmdb_id=self.tmdb_id)
        response = client.post(self.url)
        assert response.url == movie.get_absolute_url()
        assert Movie.objects.count() == 1
