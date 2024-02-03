import httpx
from django.conf import settings


def get_client(
    *,
    headers=None,
    follow_redirects=True,
    timeout=5,
    **kwargs,
) -> httpx.AsyncClient:
    """Returns HTTP client with default settings."""
    return httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=follow_redirects,
        headers={
            "User-Agent": settings.USER_AGENT,
            **(headers or {}),
        },
        **kwargs,
    )
