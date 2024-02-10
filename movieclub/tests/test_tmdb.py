import http

import httpx

from movieclub import tmdb


class TestMovieDetail:
    def test_ok(self):
        def _handle(request):
            if "credits" in str(request.url):
                json = {
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
                }
            else:
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
                }
            return httpx.Response(http.HTTPStatus.OK, json=json)

        client = httpx.Client(transport=httpx.MockTransport(_handle))
        movie = tmdb.get_movie_detail(client, 12345)

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

        movies = tmdb.search_movies(client, query={"Wick"})
        assert len(movies) == 1
        movie = movies[0]
        assert movie.id == 603692
        assert (
            movie.poster_path
            == "https://image.tmdb.org/t/p/original/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg"
        )
        assert movie.title == "John Wick: Chapter 4"
