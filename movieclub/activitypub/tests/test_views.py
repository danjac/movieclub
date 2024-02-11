import http

import pytest
from django.urls import reverse, reverse_lazy


class TestWebfinger:
    url = reverse_lazy("activitypub:webfinger")

    @pytest.mark.django_db()
    def test_get_ok(self, client, site, user):
        response = client.get(
            self.url, {"resource": f"acct:{user.username}@{site.domain}"}
        )
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_not_local(self, client, user):
        response = client.get(
            self.url, {"resource": f"acct:{user.username}@randomsite.com"}
        )
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.django_db()
    def test_user_not_found(self, client):
        response = client.get(self.url, {"resource": "acct:tester@omain"})
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.django_db()
    def test_resource_param_missing(self, client):
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.NOT_FOUND


class TestNodeInfo:
    url = reverse_lazy("activitypub:nodeinfo")

    @pytest.mark.django_db()
    def test_get(self, client, user):
        response = client.get(self.url)
        assert response.json()["usage"]["users"]["total"] == 1
        assert response.status_code == http.HTTPStatus.OK


class TestLocalUser:
    @pytest.mark.django_db()
    def test_get(self, client, user_with_keypair):
        response = client.get(
            reverse(
                "activitypub:local_user",
                args=[user_with_keypair.username],
            )
        )

        assert response.status_code == http.HTTPStatus.OK
