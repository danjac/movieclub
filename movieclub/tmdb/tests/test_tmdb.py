import httpx
import pytest

from movieclub.releases.tests.factories import create_genre
from movieclub.tmdb import models, populate_movie, populate_tv_show


class TestPopulateTVShow:
    @pytest.mark.django_db()
    def test_ok(self, mocker):
        create_genre(tmdb_id=9648, name="Mystery")
        create_genre(tmdb_id=80, name="Crime")
        create_genre(tmdb_id=18, name="Drama")

        mocker.patch(
            "movieclub.tmdb.api.get_tv_show_detail",
            return_value=models.TVShowDetail(
                id=484,
                name="Murder, She Wrote",
                overview="An unassuming mystery writer turned sleuth uses her professional insight to help solve real-life homicide cases.",
                first_air_date="1984-9-30",
                last_air_date="1996-5-19",
                backdrop_path="https://image.tmdb.org/t/p/original/8k67coQA1KXLg0HmB5PJBBTL6dX.jpg",
                poster_path="https://image.tmdb.org/t/p/original/3UxBFG4fiuZ0P9n2sCrjXh64Avy.jpg",
                tagline="",
                homepage="",
                number_of_episodes=264,
                number_of_seasons=12,
                genres=[
                    models.Genre(id=9648, name="Mystery"),
                    models.Genre(id=80, name="Crime"),
                    models.Genre(id=18, name="Drama"),
                ],
                cast_members=[
                    models.CastMember(
                        id=14730,
                        gender=1,
                        name="Angela Lansbury",
                        profile_path="https://image.tmdb.org/t/p/original/sNIHnWjXEpBcTjRxzmrwuJyHqfi.jpg",
                        order=0,
                        character="Jessica Fletcher",
                    )
                ],
                crew_members=[
                    models.CrewMember(
                        id=14930,
                        gender=2,
                        name="John Addison",
                        profile_path="",
                        job="Main Title Theme Composer",
                    ),
                    models.CrewMember(
                        id=372172,
                        gender=2,
                        name="Robert F. O'Neill",
                        profile_path="",
                        job="Producer",
                    ),
                    models.CrewMember(
                        id=1217028,
                        gender=0,
                        name="Douglas Benton",
                        profile_path="",
                        job="Producer",
                    ),
                    models.CrewMember(
                        id=14730,
                        gender=1,
                        name="Angela Lansbury",
                        profile_path="https://image.tmdb.org/t/p/original/sNIHnWjXEpBcTjRxzmrwuJyHqfi.jpg",
                        job="Producer",
                    ),
                    models.CrewMember(
                        id=151395,
                        gender=2,
                        name="Peter S. Fischer",
                        profile_path="",
                        job="Executive Producer",
                    ),
                    models.CrewMember(
                        id=42058,
                        gender=2,
                        name="William Link",
                        profile_path="",
                        job="Executive Producer",
                    ),
                    models.CrewMember(
                        id=42057,
                        gender=2,
                        name="Richard Levinson",
                        profile_path="",
                        job="Executive Producer",
                    ),
                ],
                origin_country=["US"],
            ),
        )

        tv_show = populate_tv_show(httpx.Client(), 484)

        assert tv_show.title == "Murder, She Wrote"
        assert tv_show.num_episodes == 264
        assert tv_show.num_seasons == 12

        assert tv_show.genres.count() == 3

        assert tv_show.cast_members.count() == 1
        assert tv_show.crew_members.count() == 7

        assert tv_show.countries == ["US"]


class TestPopulateMovie:
    @pytest.mark.django_db()
    def test_ok(self, mocker):
        create_genre(tmdb_id=28, name="Action")
        create_genre(tmdb_id=53, name="Thriller")
        mocker.patch(
            "movieclub.tmdb.api.get_movie_detail",
            return_value=models.MovieDetail(
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
                    models.Country(
                        iso_3166_1="US",
                        name="United States of America",
                    ),
                ],
                genres=[
                    models.Genre(id=28, name="Action"),
                    models.Genre(id=53, name="Thriller"),
                ],
                cast_members=[
                    models.CastMember(
                        gender=2,
                        id=6384,
                        name="Keanu Reeves",
                        profile_path="https://example.com/profile.jpg",
                        order=0,
                    )
                ],
                crew_members=[
                    models.CrewMember(
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
