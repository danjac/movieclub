import httpx
import pytest

from movieclub import tmdb
from movieclub.releases.tests.factories import create_genre
from movieclub.releases.tmdb import populate_movie


class TestPopulateMovie:
    @pytest.mark.django_db()
    def test_ok(self, mocker):
        create_genre(tmdb_id=28, name="Action")
        create_genre(tmdb_id=53, name="Thriller")
        mocker.patch(
            "movieclub.tmdb.get_movie_detail",
            return_value=tmdb.MovieDetail(
                id=12345,
                title="John Wick",
                homepage="https://www.lionsgate.com/movies/john-wick",
                original_language="en",
                original_title="John Wick",
                backdrop_path="https://example.com/poster.jpg",
                poster_path="https://example.com/backdrop.jpg",
                runtime=101,
                release_date="2014-10-22",
                overview="Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.",
                tagline="Don't set him off.",
                production_countries=[
                    tmdb.Country(
                        iso_3166_1="US",
                        name="United States of America",
                    ),
                ],
                genres=[
                    tmdb.Genre(id=28, name="Action"),
                    tmdb.Genre(id=53, name="Thriller"),
                ],
                cast_members=[
                    tmdb.CastMember(
                        gender=2,
                        id=6384,
                        name="Keanu Reeves",
                        profile_path="https://example.com/profile.jpg",
                        order=0,
                    )
                ],
                crew_members=[
                    tmdb.CrewMember(
                        gender=2,
                        id=40644,
                        name="Chad Stahelski",
                        profile_path="https://example.com/profile2.jpg",
                        job="Director",
                    )
                ],
            ),
        )

        movie = populate_movie(httpx.Client(), 12345)

        assert movie.title == "John Wick"
        assert movie.runtime == 101
        assert movie.countries[0].code == "US"
        assert movie.genres.count() == 2
        assert movie.cast_members.count() == 1
        assert movie.crew_members.count() == 1
