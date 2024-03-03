import http
import urllib

import httpx
import pytest
from django.core.signing import Signer
from django.urls import reverse, reverse_lazy

from movieclub.releases.tests.factories import create_movie
from movieclub.tests.factories import create_batch


class TestLandingPage:
    url = reverse_lazy("landing_page")

    @pytest.mark.django_db()
    def test_get(self, client):
        create_batch(create_movie, 12)
        assert client.get(self.url).status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_empty(self, client):
        assert client.get(self.url).status_code == http.HTTPStatus.OK


class TestAcceptCookies:
    url = reverse_lazy("accept_cookies")

    @pytest.mark.django_db()
    def test_post(self, client):
        response = client.post(reverse("accept_cookies"))
        assert response.status_code == http.HTTPStatus.OK
        assert "accept-cookies" in response.cookies


class TestCoverImage:
    cover_url = "http://example.com/test.png"

    def get_url(self, width, height, url):
        return (
            reverse(
                "cover_image",
                kwargs={
                    "height": height,
                    "width": width,
                },
            )
            + "?"
            + urllib.parse.urlencode({"url": url})
        )

    def encode_url(self, url):
        return Signer().sign(url)

    @pytest.mark.django_db()
    def test_ok(self, client, db, mocker):
        def _handler(request):
            return httpx.Response(http.HTTPStatus.OK, content=b"")

        mock_client = httpx.Client(transport=httpx.MockTransport(_handler))
        mocker.patch("movieclub.views.get_client", return_value=mock_client)
        mocker.patch("PIL.Image.open", return_value=mocker.Mock())
        response = client.get(self.get_url(100, 150, self.encode_url(self.cover_url)))
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_not_accepted_size(self, client, db, mocker):
        response = client.get(self.get_url(500, 1000, self.encode_url(self.cover_url)))
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.django_db()
    def test_missing_url_param(self, client, db, mocker):
        response = client.get(
            reverse("cover_image", kwargs={"width": 100, "height": 150})
        )
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.django_db()
    def test_unsigned_url(self, client, db):
        response = client.get(self.get_url(100, 150, self.cover_url))
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.django_db()
    def test_failed_download(self, client, db, mocker):
        def _handler(request):
            raise httpx.HTTPError("invalid")

        mock_client = httpx.Client(transport=httpx.MockTransport(_handler))
        mocker.patch("movieclub.views.get_client", return_value=mock_client)

        response = client.get(self.get_url(100, 150, self.encode_url(self.cover_url)))
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.django_db()
    def test_failed_process(self, client, db, mocker):
        def _handler(request):
            return httpx.Response(http.HTTPStatus.OK, content=b"")

        mock_client = httpx.Client(transport=httpx.MockTransport(_handler))
        mocker.patch("movieclub.views.get_client", return_value=mock_client)
        mocker.patch("PIL.Image.open", side_effect=IOError())
        response = client.get(self.get_url(100, 150, self.encode_url(self.cover_url)))
        assert response.status_code == http.HTTPStatus.NOT_FOUND
