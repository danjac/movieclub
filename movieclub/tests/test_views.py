import http

import pytest
from django.urls import reverse_lazy


class TestLandingPage:
    url = reverse_lazy("landing_page")

    @pytest.mark.django_db()
    def test_get(self, client):
        assert client.get(self.url).status_code == http.HTTPStatus.OK
