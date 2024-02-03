from typing import Final
from urllib.parse import urljoin

import httpx
from django.conf import settings

BASE_URL: Final = "https://api.themoviedb.org/3/"
BASE_IMAGE_URL: Final = "https://image.tmdb.org/t/p/original/"


async def search_movies(client: httpx.AsyncClient, query: str) -> dict:
    """Search for movies."""
    return await _get_json(client, "search/movie", {"query": query})


async def search_tv_shows(client: httpx.AsyncClient, query: str) -> dict:
    """Search for movies."""
    return await _get_json(client, "search/tv", {"query": query})


async def get_image(client: httpx.AsyncClient, path: str) -> bytes:
    """Fetch image from Tmdb."""
    response = await client.get(urljoin(BASE_IMAGE_URL, path[1:]))
    response.raise_for_status()
    return response.content


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
