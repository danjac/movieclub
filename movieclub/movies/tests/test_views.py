import functools
import http

import pytest
from django.urls import reverse, reverse_lazy

from movieclub.movies import views
from movieclub.movies.models import Movie
from movieclub.movies.tests.factories import acreate_movie, create_movie
from movieclub.movies.tests.mocks import credits_json, movie_json, search_results_json
from movieclub.tests.factories import create_batch
from movieclub.users.models import User
from movieclub.users.tests.factories import acreate_user


async def _auser_to_request(request):
    user = await acreate_user()

    async def _auser(request):
        return await User.objects.aget(pk=user.pk)

    request.auser = functools.partial(_auser, request)
    return request


class TestIndex:
    url = reverse_lazy("movies:index")

    @pytest.mark.django_db()
    def test_get(self, client):
        create_batch(create_movie, 10)
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.OK


class TestDetail:
    @pytest.mark.django_db()
    def test_get(self, client):
        movie = create_movie()
        response = client.get(movie.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK


class TestSearchTmdb:
    url = reverse_lazy("movies:search_tmdb")

    @pytest.mark.asyncio()
    @pytest.mark.django_db(transaction=True)
    async def test_get(self, rf, httpx_mock):
        httpx_mock.add_response(
            url="https://api.themoviedb.org/3/search/movie?query=Wick",
            json=search_results_json(),
        )
        request = rf.get(self.url, {"query": "Wick"})
        response = await views.search_tmdb(request)
        assert response.status_code == http.HTTPStatus.OK


class TestAddMovie:
    tmdb_id = 245891

    @pytest.mark.asyncio()
    @pytest.mark.django_db(transaction=True)
    async def test_post(self, rf, httpx_mock, mocker):
        httpx_mock.add_response(
            url=f"https://api.themoviedb.org/3/movie/{self.tmdb_id}",
            json=movie_json(),
        )

        httpx_mock.add_response(
            url=f"https://api.themoviedb.org/3/movie/{self.tmdb_id}/credits",
            json=credits_json(),
        )

        request = rf.post(reverse("movies:add_movie", args=[self.tmdb_id]))
        request._messages = mocker.Mock()

        await _auser_to_request(request)

        response = await views.add_movie(request, self.tmdb_id)

        movie = await Movie.objects.aget()
        assert movie.tmdb_id == self.tmdb_id
        assert response.url == movie.get_absolute_url()

    @pytest.mark.asyncio()
    @pytest.mark.django_db(transaction=True)
    async def test_post_exists(self, rf):
        movie = await acreate_movie(tmdb_id=self.tmdb_id)
        request = rf.post(reverse("movies:add_movie", args=[self.tmdb_id]))

        await _auser_to_request(request)

        response = await views.add_movie(request, self.tmdb_id)

        assert movie.tmdb_id == self.tmdb_id
        assert response.url == movie.get_absolute_url()
