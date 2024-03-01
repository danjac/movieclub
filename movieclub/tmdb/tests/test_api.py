import http

import httpx

from movieclub.tmdb import api


class TestTVShowDetail:
    def test_ok(self):
        def _handle(request):
            json = {
                "adult": False,
                "backdrop_path": "/8k67coQA1KXLg0HmB5PJBBTL6dX.jpg",
                "created_by": [
                    {
                        "id": 42057,
                        "credit_id": "52537a3e19c295794018274b",
                        "name": "Richard Levinson",
                        "gender": 2,
                        "profile_path": None,
                    },
                    {
                        "id": 42058,
                        "credit_id": "52537a3f19c295794018275d",
                        "name": "William Link",
                        "gender": 2,
                        "profile_path": None,
                    },
                    {
                        "id": 151395,
                        "credit_id": "559209c9c3a368080400255c",
                        "name": "Peter S. Fischer",
                        "gender": 2,
                        "profile_path": None,
                    },
                ],
                "episode_run_time": [45],
                "first_air_date": "1984-09-30",
                "genres": [
                    {"id": 9648, "name": "Mystery"},
                    {"id": 80, "name": "Crime"},
                    {"id": 18, "name": "Drama"},
                ],
                "homepage": "",
                "id": 484,
                "in_production": False,
                "languages": ["en"],
                "last_air_date": "1996-05-19",
                "last_episode_to_air": {
                    "id": 24006,
                    "name": "Death by Demographics",
                    "overview": "In San Francisco, a radio station's new manager is trying to change their image by firing every staff member who is past a certain age and playing music for teen-agers only.",
                    "vote_average": 0.0,
                    "vote_count": 0,
                    "air_date": "1996-05-19",
                    "episode_number": 24,
                    "episode_type": "finale",
                    "production_code": "",
                    "runtime": 45,
                    "season_number": 12,
                    "show_id": 484,
                    "still_path": "/54UiWLIrDK39yn53SVfTuarYVdv.jpg",
                },
                "name": "Murder, She Wrote",
                "next_episode_to_air": None,
                "networks": [
                    {
                        "id": 16,
                        "logo_path": "/wju8KhOUsR5y4bH9p3Jc50hhaLO.png",
                        "name": "CBS",
                        "origin_country": "US",
                    }
                ],
                "number_of_episodes": 264,
                "number_of_seasons": 12,
                "origin_country": ["US"],
                "original_language": "en",
                "original_name": "Murder, She Wrote",
                "overview": "An unassuming mystery writer turned sleuth uses her professional insight to help solve real-life homicide cases.",
                "popularity": 177.675,
                "poster_path": "/3UxBFG4fiuZ0P9n2sCrjXh64Avy.jpg",
                "production_companies": [
                    {
                        "id": 26727,
                        "logo_path": "/jeTxdjXhzgKZyLr3l9MllkTn3fy.png",
                        "name": "Universal Television",
                        "origin_country": "US",
                    },
                    {
                        "id": 56845,
                        "logo_path": None,
                        "name": "Corymore Productions",
                        "origin_country": "US",
                    },
                ],
                "production_countries": [
                    {"iso_3166_1": "US", "name": "United States of America"}
                ],
                "seasons": [
                    {
                        "air_date": "1984-09-30",
                        "episode_count": 22,
                        "id": 1371,
                        "name": "Season 1",
                        "overview": "",
                        "poster_path": "/iRNXE5xDeSGpYGf8tBTlItiXNIs.jpg",
                        "season_number": 1,
                        "vote_average": 7.2,
                    },
                    {
                        "air_date": "1985-09-29",
                        "episode_count": 22,
                        "id": 1372,
                        "name": "Season 2",
                        "overview": "",
                        "poster_path": "/rBRBZ8g85mfHUk6aSGirl4g7qjk.jpg",
                        "season_number": 2,
                        "vote_average": 7.1,
                    },
                    {
                        "air_date": "1986-09-28",
                        "episode_count": 22,
                        "id": 1373,
                        "name": "Season 3",
                        "overview": "",
                        "poster_path": "/dIeLpfR0gxd7TsMlpPobQXH0ypr.jpg",
                        "season_number": 3,
                        "vote_average": 7.2,
                    },
                ],
                "spoken_languages": [
                    {"english_name": "English", "iso_639_1": "en", "name": "English"}
                ],
                "status": "Ended",
                "tagline": "",
                "type": "Scripted",
                "vote_average": 7.584,
                "vote_count": 334,
                "credits": {
                    "cast": [
                        {
                            "adult": False,
                            "gender": 1,
                            "id": 14730,
                            "known_for_department": "Acting",
                            "name": "Angela Lansbury",
                            "original_name": "Angela Lansbury",
                            "popularity": 21.063,
                            "profile_path": "/sNIHnWjXEpBcTjRxzmrwuJyHqfi.jpg",
                            "character": "Jessica Fletcher",
                            "credit_id": "52537a3e19c2957940182677",
                            "order": 0,
                        }
                    ],
                    "crew": [
                        {
                            "adult": False,
                            "gender": 2,
                            "id": 14930,
                            "known_for_department": "Sound",
                            "name": "John Addison",
                            "original_name": "John Addison",
                            "popularity": 1.101,
                            "profile_path": None,
                            "credit_id": "5efb56035437f500388dbadd",
                            "department": "Sound",
                            "job": "Main Title Theme Composer",
                        },
                        {
                            "adult": False,
                            "gender": 1,
                            "id": 14730,
                            "known_for_department": "Acting",
                            "name": "Angela Lansbury",
                            "original_name": "Angela Lansbury",
                            "popularity": 21.063,
                            "profile_path": "/sNIHnWjXEpBcTjRxzmrwuJyHqfi.jpg",
                            "credit_id": "52537a3f19c2957940182767",
                            "department": "Production",
                            "job": "Producer",
                        },
                        {
                            "adult": False,
                            "gender": 2,
                            "id": 372172,
                            "known_for_department": "Production",
                            "name": "Robert F. O'Neill",
                            "original_name": "Robert F. O'Neill",
                            "popularity": 2.187,
                            "profile_path": None,
                            "credit_id": "52537a4019c2957940182877",
                            "department": "Production",
                            "job": "Producer",
                        },
                        {
                            "adult": False,
                            "gender": 0,
                            "id": 1217028,
                            "known_for_department": "Production",
                            "name": "Douglas Benton",
                            "original_name": "Douglas Benton",
                            "popularity": 0.926,
                            "profile_path": None,
                            "credit_id": "52537a4119c295794018292d",
                            "department": "Production",
                            "job": "Producer",
                        },
                        {
                            "adult": False,
                            "gender": 2,
                            "id": 42057,
                            "known_for_department": "Writing",
                            "name": "Richard Levinson",
                            "original_name": "Richard Levinson",
                            "popularity": 2.096,
                            "profile_path": None,
                            "credit_id": "52537a3f19c29579401827c1",
                            "department": "Production",
                            "job": "Executive Producer",
                        },
                        {
                            "adult": False,
                            "gender": 2,
                            "id": 42058,
                            "known_for_department": "Writing",
                            "name": "William Link",
                            "original_name": "William Link",
                            "popularity": 1.771,
                            "profile_path": None,
                            "credit_id": "52537a3f19c295794018281b",
                            "department": "Production",
                            "job": "Executive Producer",
                        },
                        {
                            "adult": False,
                            "gender": 2,
                            "id": 151395,
                            "known_for_department": "Writing",
                            "name": "Peter S. Fischer",
                            "original_name": "Peter S. Fischer",
                            "popularity": 1.607,
                            "profile_path": None,
                            "credit_id": "52537a4019c29579401828d1",
                            "department": "Production",
                            "job": "Executive Producer",
                        },
                    ],
                },
            }

            return httpx.Response(http.HTTPStatus.OK, json=json)

        client = httpx.Client(transport=httpx.MockTransport(_handle))
        show = api.get_tv_show_detail(client, 484)

        assert show.id == 484
        assert show.name == "Murder, She Wrote"
        assert len(show.genres) == 3
        assert len(show.origin_country) == 1

        assert (
            show.poster_path
            == "https://image.tmdb.org/t/p/original/3UxBFG4fiuZ0P9n2sCrjXh64Avy.jpg"
        )

        cast = show.cast_members[0]

        assert cast.name == "Angela Lansbury"
        assert cast.order == 0
        assert cast.character == "Jessica Fletcher"

        assert (
            cast.profile_path
            == "https://image.tmdb.org/t/p/original/sNIHnWjXEpBcTjRxzmrwuJyHqfi.jpg"
        )

        crew = show.crew_members[0]

        assert crew.name == "John Addison"
        assert crew.job == "Main Title Theme Composer"


class TestMovieDetail:
    def test_ok(self):
        def _handle(request):
            json = {
                "adult": False,
                "backdrop_path": "/7dzngS8pLkGJpyeskCFcjPO9qLF.jpg",
                "belongs_to_collection": {
                    "id": 404609,
                    "name": "John Wick Collection",
                    "poster_path": "/xUidyvYFsbbuExifLkslpcd8SMc.jpg",
                    "backdrop_path": "/fSwYa5q2xRkBoOOjueLpkLf3N1m.jpg",
                },
                "budget": 20000000,
                "genres": [
                    {"id": 28, "name": "Action"},
                    {"id": 53, "name": "Thriller"},
                ],
                "homepage": "https://www.lionsgate.com/movies/john-wick",
                "id": 12345,
                "imdb_id": "tt2911666",
                "original_language": "en",
                "original_title": "John Wick",
                "overview": "Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.",
                "popularity": 53.89,
                "poster_path": "/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg",
                "production_companies": [
                    {
                        "id": 23008,
                        "logo_path": "/5SarYupipdiejsEqUkwu1SpYfru.png",
                        "name": "87Eleven",
                        "origin_country": "US",
                    },
                    {
                        "id": 36259,
                        "logo_path": None,
                        "name": "DefyNite Films",
                        "origin_country": "US",
                    },
                    {
                        "id": 36433,
                        "logo_path": None,
                        "name": "MJW Films",
                        "origin_country": "US",
                    },
                    {
                        "id": 3528,
                        "logo_path": "/cCzCClIzIh81Fa79hpW5nXoUsHK.png",
                        "name": "Thunder Road",
                        "origin_country": "US",
                    },
                ],
                "production_countries": [
                    {"iso_3166_1": "US", "name": "United States of America"}
                ],
                "release_date": "2014-10-22",
                "revenue": 88761661,
                "runtime": 101,
                "spoken_languages": [
                    {
                        "english_name": "Hungarian",
                        "iso_639_1": "hu",
                        "name": "Magyar",
                    },
                    {
                        "english_name": "English",
                        "iso_639_1": "en",
                        "name": "English",
                    },
                    {
                        "english_name": "Russian",
                        "iso_639_1": "ru",
                        "name": "P\u0443\u0441\u0441\u043a\u0438\u0439",
                    },
                ],
                "status": "Released",
                "tagline": "Don't set him off.",
                "title": "John Wick",
                "video": False,
                "vote_average": 7.425,
                "vote_count": 18346,
                "credits": {
                    "id": 12345,
                    "cast": [
                        {
                            "adult": False,
                            "gender": 2,
                            "id": 6384,
                            "known_for_department": "Acting",
                            "name": "Keanu Reeves",
                            "original_name": "Keanu Reeves",
                            "popularity": 63.203,
                            "profile_path": "/4D0PpNI0kmP58hgrwGC3wCjxhnm.jpg",
                            "cast_id": 6,
                            "character": "John Wick",
                            "credit_id": "52fe4f0cc3a36847f82b9c41",
                            "order": 0,
                        },
                    ],
                    "crew": [
                        {
                            "adult": False,
                            "gender": 2,
                            "id": 40644,
                            "known_for_department": "Directing",
                            "name": "Chad Stahelski",
                            "original_name": "Chad Stahelski",
                            "popularity": 16.824,
                            "profile_path": "/eRCryGwKDH4XqUlrdkERmeBWPo8.jpg",
                            "credit_id": "5f70bc15196757003a8bfe45",
                            "department": "Directing",
                            "job": "Director",
                        },
                    ],
                },
            }
            return httpx.Response(http.HTTPStatus.OK, json=json)

        client = httpx.Client(transport=httpx.MockTransport(_handle))
        movie = api.get_movie_detail(client, 12345)

        assert movie.id == 12345
        assert movie.title == "John Wick"
        assert len(movie.genres) == 2
        assert len(movie.production_countries) == 1

        assert (
            movie.poster_path
            == "https://image.tmdb.org/t/p/original/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg"
        )

        cast = movie.cast_members[0]

        assert cast.name == "Keanu Reeves"
        assert cast.order == 0
        assert cast.character == "John Wick"
        assert (
            cast.profile_path
            == "https://image.tmdb.org/t/p/original/4D0PpNI0kmP58hgrwGC3wCjxhnm.jpg"
        )

        crew = movie.crew_members[0]

        assert crew.name == "Chad Stahelski"
        assert crew.job == "Director"


class TestSearchTVShows:
    def test_ok(self):
        def _handle(request):
            return httpx.Response(
                http.HTTPStatus.OK,
                json={
                    "page": 1,
                    "results": [
                        {
                            "adult": False,
                            "backdrop_path": "/8k67coQA1KXLg0HmB5PJBBTL6dX.jpg",
                            "genre_ids": [9648, 80, 18],
                            "id": 484,
                            "origin_country": ["US"],
                            "original_language": "en",
                            "original_name": "Murder, She Wrote",
                            "overview": "An unassuming mystery writer turned sleuth uses her professional insight to help solve real-life homicide cases.",
                            "popularity": 177.675,
                            "poster_path": "/3UxBFG4fiuZ0P9n2sCrjXh64Avy.jpg",
                            "first_air_date": "1984-09-30",
                            "name": "Murder, She Wrote",
                            "vote_average": 7.584,
                            "vote_count": 334,
                        }
                    ],
                    "total_pages": 1,
                    "total_results": 1,
                },
            )

        client = httpx.Client(transport=httpx.MockTransport(_handle))

        shows = api.search_tv_shows(client, query={"murder"})
        assert len(shows) == 1
        show = shows[0]
        assert show.id == 484
        assert (
            show.poster_path
            == "https://image.tmdb.org/t/p/original/3UxBFG4fiuZ0P9n2sCrjXh64Avy.jpg"
        )
        assert show.name == "Murder, She Wrote"


class TestSearchMovies:
    def test_ok(self):
        def _handle(request):
            return httpx.Response(
                http.HTTPStatus.OK,
                json={
                    "results": [
                        {
                            "adult": False,
                            "backdrop_path": "/tfw5LKySp7uEYJ3CUuD4TKx3s8y.jpg",
                            "genre_ids": [28, 53, 80],
                            "id": 603692,
                            "original_language": "en",
                            "original_title": "John Wick: Chapter 4",
                            "overview": "With the price on his head ever increasing, John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe and forces that turn old friends into foes.",
                            "popularity": 287.885,
                            "poster_path": "/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg",
                            "release_date": "2023-03-22",
                            "title": "John Wick: Chapter 4",
                            "video": False,
                            "vote_average": 7.755,
                            "vote_count": 5513,
                        }
                    ]
                },
            )

        client = httpx.Client(transport=httpx.MockTransport(_handle))

        movies = api.search_movies(client, query={"Wick"})
        assert len(movies) == 1
        movie = movies[0]
        assert movie.id == 603692
        assert (
            movie.poster_path
            == "https://image.tmdb.org/t/p/original/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg"
        )
        assert movie.title == "John Wick: Chapter 4"
