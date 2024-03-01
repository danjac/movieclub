from __future__ import annotations

from typing import TYPE_CHECKING, Final
from urllib.parse import urljoin

import attrs
from django.conf import settings

from movieclub.tmdb.models import (
    CastMember,
    Country,
    CrewMember,
    Genre,
    Movie,
    MovieDetail,
    TVShow,
    TVShowDetail,
)

if TYPE_CHECKING:  # pragma: no cover
    import httpx


BASE_URL: Final = "https://api.themoviedb.org/3/"


def search_movies(client: httpx.Client, query: str) -> list[Movie]:
    """Searches movies."""
    response = _fetch_json(
        client,
        "search/movie",
        params={
            "query": query,
        },
    )

    return [_populate_obj(Movie, result) for result in response["results"]]


def search_tv_shows(client: httpx.Client, query: str) -> list[TVShow]:
    """Searches movies."""
    response = _fetch_json(
        client,
        "search/tv",
        params={
            "query": query,
        },
    )

    return [_populate_obj(TVShow, result) for result in response["results"]]


def get_movie_detail(client: httpx.Client, tmdb_id: int) -> MovieDetail:
    """Fetch details from TMDB"""

    movie_data = _fetch_json(client, f"movie/{tmdb_id}?append_to_response=credits")
    credits_data = movie_data.get("credits", {})

    return _populate_obj(
        MovieDetail,
        movie_data,
        cast_members=[
            _populate_obj(CastMember, item)
            for item in credits_data.get(
                "cast",
                [],
            )
        ],
        crew_members=[
            _populate_obj(CrewMember, item)
            for item in credits_data.get(
                "crew",
                [],
            )
        ],
        genres=[
            _populate_obj(Genre, item)
            for item in movie_data.get(
                "genres",
                [],
            )
        ],
        production_countries=[
            _populate_obj(Country, item)
            for item in movie_data.get(
                "production_countries",
                [],
            )
        ],
    )


def get_tv_show_detail(client: httpx.Client, tmdb_id: int) -> TVShowDetail:
    """Returns details on TV show."""
    show_data = _fetch_json(client, f"tv/{tmdb_id}?append_to_response=credits")
    credits_data = show_data.get("credits", {})

    return _populate_obj(
        TVShowDetail,
        show_data,
        cast_members=[
            _populate_obj(CastMember, item)
            for item in credits_data.get(
                "cast",
                [],
            )
        ],
        crew_members=[
            _populate_obj(CrewMember, item)
            for item in credits_data.get(
                "crew",
                [],
            )
        ],
        genres=[
            _populate_obj(Genre, item)
            for item in show_data.get(
                "genres",
                [],
            )
        ],
    )


def _fetch_json(
    client: httpx.Client,
    path: str,
    headers: dict | None = None,
    **kwargs,
) -> dict:
    response = client.get(
        urljoin(BASE_URL, path),
        headers={
            "Authorization": f"Bearer {settings.TMDB_API_ACCESS_TOKEN}",
            **(headers or {}),
        },
        **kwargs,
    )

    response.raise_for_status()

    return response.json()


def _populate_obj(cls: type, data: dict, **kwargs):
    fields = [f.name for f in attrs.fields(cls)]
    return cls(**{k: v for k, v in (data | kwargs).items() if k in fields})
