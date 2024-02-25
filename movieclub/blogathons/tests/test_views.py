import datetime
import http

import pytest
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from movieclub.blogathons.models import Blogathon
from movieclub.blogathons.tests.factories import create_blogathon
from movieclub.tests.factories import create_batch


class TestBlogathonList:
    url = reverse_lazy("blogathons:blogathon_list")

    @pytest.mark.django_db()
    def test_get(self, client):
        create_batch(create_blogathon, 3)
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.OK


class TestAddBlogathon:
    url = reverse_lazy("blogathons:add_blogathon")

    @pytest.mark.django_db()
    def test_get(self, client, auth_user):
        response = client.get(self.url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post(self, client, auth_user):
        starts = timezone.now() + datetime.timedelta(days=7)
        ends = starts + datetime.timedelta(days=14)
        response = client.post(
            self.url,
            {
                "starts": starts.strftime("%Y-%m-%d"),
                "ends": ends.strftime("%Y-%m-%d"),
                "name": "test",
                "description": "test",
            },
        )
        assert response.url == reverse("blogathons:blogathon_list")

        blogathon = Blogathon.objects.get()
        assert blogathon.organizer == auth_user


class TestBlogathonDetail:
    @pytest.mark.django_db()
    def test_get(self, client, auth_user, public_blogathon):
        response = client.get(public_blogathon.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK
