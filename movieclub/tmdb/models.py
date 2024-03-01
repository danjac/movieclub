from __future__ import annotations

import datetime
from typing import Final
from urllib.parse import urljoin

import attrs

BASE_IMAGE_URL: Final = "https://image.tmdb.org/t/p/original/"


def _image_url(path: str) -> str:
    """Returns URL to original image."""
    return urljoin(BASE_IMAGE_URL, path[1:]) if path else ""


def _release_date(value: str) -> datetime.date | None:
    return datetime.datetime.strptime(value, "%Y-%m-%d").date() if value else None


@attrs.define(kw_only=True)
class Person:
    """Tmdb Person."""

    id: int
    gender: int
    name: str

    profile_path: str = attrs.field(converter=_image_url, default="")


@attrs.define(kw_only=True)
class CastMember(Person):
    """Tmdb Cast member."""

    order: int = 0
    character: str = ""


@attrs.define(kw_only=True)
class CrewMember(Person):
    """Tmdb Cast member."""

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

    imdb_id: str = attrs.field(
        converter=attrs.converters.default_if_none(""),  # type: ignore[misc]
        default="",
    )

    tagline: str = ""
    homepage: str = ""

    original_title: str = ""
    original_language: str = "en"

    runtime: int = 0

    genres: list = attrs.field(default=attrs.Factory(list))

    cast_members: list = attrs.field(default=attrs.Factory(list))
    crew_members: list = attrs.field(default=attrs.Factory(list))

    production_countries: list = attrs.field(default=attrs.Factory(list))


@attrs.define(kw_only=True)
class TVShow:
    """Tmdb Search result."""

    id: int
    name: str

    overview: str = ""

    first_air_date: datetime.date | None = attrs.field(
        converter=_release_date, default=None
    )

    last_air_date: datetime.date | None = attrs.field(
        converter=_release_date, default=None
    )

    backdrop_path: str = attrs.field(converter=_image_url, default="")
    poster_path: str = attrs.field(converter=_image_url, default="")


@attrs.define(kw_only=True)
class TVShowDetail(TVShow):
    """Tmdb Movie."""

    tagline: str = ""
    homepage: str = ""

    number_of_episodes: int = 0
    number_of_seasons: int = 0

    genres: list = attrs.field(default=attrs.Factory(list))

    cast_members: list = attrs.field(default=attrs.Factory(list))
    crew_members: list = attrs.field(default=attrs.Factory(list))

    origin_country: list = attrs.field(default=attrs.Factory(list))
