from __future__ import annotations

from typing import TYPE_CHECKING, Final
from urllib.parse import urljoin

import arrow
import attrs
from django.conf import settings

if TYPE_CHECKING:  # pragma: no cover
    import datetime

    import httpx


BASE_URL: Final = "https://api.themoviedb.org/3/"
BASE_IMAGE_URL: Final = "https://image.tmdb.org/t/p/original/"


def _image_url(path: str) -> str:
    """Returns URL to original image."""
    return urljoin(BASE_IMAGE_URL, path[1:]) if path else ""


def _release_date(value: str) -> datetime.date | None:
    return arrow.get(value).date() if value else None


@attrs.define(kw_only=True)
class Person:
    """Tmdb Person."""

    id: int
    gender: int
    name: str

    profile_path: str = attrs.field(converter=_image_url, default="")


@attrs.define(kw_only=True)
class CastMember(Person):
    """Imdb Cast member."""

    order: int = 0
    character: str = ""


@attrs.define(kw_only=True)
class CrewMember(Person):
    """Imdb Cast member."""

    job: str = ""


@attrs.define(kw_only=True)
class Genre:
    """Tmdb Person."""

    id: int
    name: str


@attrs.define(kw_only=True)
class Country:
    """Production country."""

    iso_3166_1: str
    name: str


@attrs.define(kw_only=True)
class Movie:
    """Tmdb Search result."""

    id: int
    title: str

    original_title: str = ""
    overview: str = ""

    release_date: datetime.date | None = attrs.field(
        converter=_release_date, default=None
    )

    backdrop_path: str = attrs.field(converter=_image_url, default="")
    poster_path: str = attrs.field(converter=_image_url, default="")


@attrs.define(kw_only=True)
class MovieDetail(Movie):
    """Tmdb Movie."""

    imdb_id: str = ""

    tagline: str = ""
    homepage: str = ""

    original_title: str = ""
    original_language: str = "en"

    runtime: int = 0

    genres: list = attrs.field(default=attrs.Factory(list))

    cast_members: list = attrs.field(default=attrs.Factory(list))
    crew_members: list = attrs.field(default=attrs.Factory(list))

    production_countries: list = attrs.field(default=attrs.Factory(list))


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


def get_movie_detail(client: httpx.Client, tmdb_id: int) -> MovieDetail:
    """Fetch details from TMDB"""

    movie_data = _fetch_json(client, f"movie/{tmdb_id}")
    credits_data = _fetch_json(client, f"movie/{tmdb_id}/credits")

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
