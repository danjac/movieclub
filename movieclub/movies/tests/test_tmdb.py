import pytest

from movieclub.client import get_client
from movieclub.movies import tmdb
from movieclub.movies.tests.factories import acreate_movie
from movieclub.movies.tests.mocks import credits_json, movie_json


class TestGetOrCreateMovie:
    @pytest.mark.asyncio()
    @pytest.mark.django_db(transaction=True)
    async def test_existing_movie(self):
        movie = await acreate_movie()
        new_movie, created = await tmdb.get_or_create_movie(get_client(), movie.tmdb_id)
        assert created is False
        assert new_movie == movie

    @pytest.mark.asyncio()
    @pytest.mark.django_db(transaction=True)
    async def test_new_movie(self, httpx_mock):
        httpx_mock.add_response(
            url="https://api.themoviedb.org/3/movie/245891",
            json=movie_json(),
        )

        httpx_mock.add_response(
            url="https://api.themoviedb.org/3/movie/245891/credits",
            json=credits_json(),
        )

        movie, created = await tmdb.get_or_create_movie(get_client(), 245891)

        assert created is True
        assert movie.tmdb_id == 245891
        assert movie.title == "John Wick"
        assert movie.countries[0].code == "US"
        assert movie.release_date.year == 2014

        num_genres = await movie.genres.acount()
        assert num_genres == 2

        num_cast_members = await movie.cast_members.acount()
        assert num_cast_members == 43

        num_crew_members = await movie.crew_members.acount()
        assert num_crew_members == 169
