from typing import Final
from urllib.parse import urljoin

import httpx
from django.conf import settings

BASE_URL: Final = "https://api.themoviedb.org/3/"
BASE_IMAGE_URL: Final = "https://image.tmdb.org/t/p/original/"


def get_image_url(path: str) -> str:
    """Returns URL to original image."""
    return urljoin(BASE_IMAGE_URL, path[1:])


async def fetch_json(
    client: httpx.AsyncClient, path: str, *, headers: dict | None = None, **kwargs
) -> dict:
    """Fetch results from TMdB and return JSON."""

    response = await client.get(
        urljoin(BASE_URL, path),
        headers={
            "Authorization": f"Bearer {settings.MOVIECLUB_TMDB_API_ACCESS_TOKEN}",
            **(headers or {}),
        },
        **kwargs,
    )

    response.raise_for_status()

    return response.json()
