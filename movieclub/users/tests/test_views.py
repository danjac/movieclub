import http

import pytest
from django.urls import reverse


class TestUserDetails:
    @pytest.mark.django_db()
    def test_get(self, client, user):
        response = client.get(user.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK


class TestEditUserDetails:
    @pytest.mark.django_db()
    def test_get(self, client, auth_user):
        response = client.get(reverse("users:edit_user_details"))
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post(self, client, auth_user):
        response = client.post(reverse("users:edit_user_details"), {"bio": "test"})
        assert response.status_code == http.HTTPStatus.OK
