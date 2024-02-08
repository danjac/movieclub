import http

import pytest
from django.urls import reverse_lazy


class TestWebfinger:
    url = reverse_lazy("activitypub:webfinger")

    @pytest.mark.django_db()
    def test_get_ok(self, client, actor):
        response = client.get(self.url, {"resource": f"acct:{actor.get_resource()}"})
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_not_local(self, client, remote_actor):
        response = client.get(
            self.url, {"resource": f"acct:{remote_actor.get_resource()}"}
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
    def test_get(self, client, actor):
        response = client.get(self.url)
        assert response.json()["usage"]["users"]["total"] == 1
        assert response.status_code == http.HTTPStatus.OK
