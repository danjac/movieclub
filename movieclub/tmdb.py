from typing import Final
from urllib.parse import urljoin

import httpx
from django.conf import settings

BASE_URL: Final = "https://api.themoviedb.org/3/"
BASE_IMAGE_URL: Final = "https://image.tmdb.org/t/p/original/"


def get_image_url(path: str) -> str:
    """Returns URL to original image."""
    return urljoin(BASE_IMAGE_URL, path[1:])


async def search_movies(client: httpx.AsyncClient, query: str) -> dict:
    """Search for movies."""
    return await _get_json(client, "search/movie", {"query": query})


async def get_movie_genres(client: httpx.AsyncClient) -> dict:
    """Returns all movie genres."""
    return await _get_json(client, "genre/movie/list")


async def get_movie(client: httpx.AsyncClient, movie_id: int) -> dict:
    """Fetch single movie detail."""
    return await _get_json(client, f"movie/{movie_id}")


async def get_movie_credits(client: httpx.AsyncClient, movie_id: int) -> dict:
    """Fetch single movie credits."""
    return await _get_json(client, f"movie/{movie_id}/credits")


async def search_tv_series(client: httpx.AsyncClient, query: str) -> dict:
    """Search for TV series."""
    return await _get_json(client, "search/tv", {"query": query})


async def get_tv_genres(client: httpx.AsyncClient) -> dict:
    """Returns all TV genres."""
    return await _get_json(client, "genre/tv/list")


async def get_tv_series(client: httpx.AsyncClient, series_id: int) -> dict:
    """Fetch single TV series detail."""
    return await _get_json(client, f"tv/{series_id}")


async def get_season(client: httpx.AsyncClient, series_id: int, season: int) -> dict:
    """Fetech single TV series season detail."""
    return await _get_json(client, f"tv/{series_id}/{season}")


async def _get_json(
    client: httpx.AsyncClient, path: str, params: dict | None = None, **kwargs
) -> dict:
    """Fetch results from TMdB and return JSON."""

    response = await client.get(
        urljoin(BASE_URL, path),
        params={
            **(params or {}),
            "api_key": settings.MOVIECLUB_TMDB_API_KEY,
        },
        **kwargs,
    )

    response.raise_for_status()

    return response.json()
