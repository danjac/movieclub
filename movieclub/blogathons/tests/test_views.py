import datetime
import http

import pytest
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from movieclub.blogathons.models import Blogathon
from movieclub.blogathons.tests.factories import create_blogathon, create_proposal
from movieclub.tests.factories import create_batch


@pytest.fixture()
def auth_user_blogathon(auth_user):
    return create_blogathon(organizer=auth_user)


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


class TestEditBlogathon:
    @pytest.fixture()
    def url(self, auth_user_blogathon):
        return reverse("blogathons:edit_blogathon", args=[auth_user_blogathon.pk])

    @pytest.mark.django_db()
    def test_get(self, client, url):
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post(self, client, auth_user_blogathon, url):
        starts = timezone.now() + datetime.timedelta(days=7)
        ends = starts + datetime.timedelta(days=14)
        response = client.post(
            url,
            {
                "starts": starts.strftime("%Y-%m-%d"),
                "ends": ends.strftime("%Y-%m-%d"),
                "name": "test",
                "description": "test",
            },
        )

        auth_user_blogathon.refresh_from_db()

        assert response.url == auth_user_blogathon.get_absolute_url()
        assert auth_user_blogathon.name == "test"


class TestBlogathonDetail:
    @pytest.mark.django_db()
    def test_get(self, client, auth_user, public_blogathon):
        response = client.get(public_blogathon.get_absolute_url())
        assert response.status_code == http.HTTPStatus.OK


class TestBlogathonProposals:
    @pytest.mark.django_db()
    def test_get(self, client, auth_user_blogathon):
        response = client.get(
            reverse("blogathons:blogathon_proposals", args=[auth_user_blogathon.pk])
        )
        assert response.status_code == http.HTTPStatus.OK


class TestSubmitProposal:
    @pytest.fixture()
    def url(self, public_blogathon):
        return reverse("blogathons:submit_proposal", args=[public_blogathon.pk])

    @pytest.mark.django_db()
    def test_get(self, client, auth_user, url):
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_get_not_allowed(self, client, auth_user, public_blogathon, url):
        create_proposal(participant=auth_user, blogathon=public_blogathon)
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.FORBIDDEN

    @pytest.mark.django_db()
    def test_post(self, client, auth_user, public_blogathon, url):
        response = client.post(url, {"proposal": "test"})
        assert response.url == public_blogathon.get_absolute_url()
        assert public_blogathon.proposals.count() == 1


class TestPublishBlogathon:
    @pytest.mark.django_db()
    def test_post(self, client, auth_user_blogathon):
        response = client.post(
            reverse("blogathons:publish_blogathon", args=[auth_user_blogathon.pk])
        )
        assert response.url == auth_user_blogathon.get_absolute_url()
        auth_user_blogathon.refresh_from_db()
        assert auth_user_blogathon.published


class TestRespondToProposal:
    @pytest.fixture()
    def proposal(self, auth_user_blogathon):
        return create_proposal(blogathon=auth_user_blogathon)

    @pytest.fixture()
    def url(self, proposal):
        return reverse("blogathons:respond_to_proposal", args=[proposal.pk])

    @pytest.mark.django_db()
    def test_get(self, client, proposal, url):
        response = client.get(
            url, HTTP_HX_REQUEST="true", HTTP_HX_TARGET=proposal.get_hx_target()
        )
        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_post_cancel(self, client, proposal, url):
        response = client.post(
            url,
            {"action": "cancel"},
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET=proposal.get_hx_target(),
        )
        assert response.status_code == http.HTTPStatus.OK
        proposal.refresh_from_db()
        assert proposal.status_changed_at is None
        assert proposal.is_submitted()

    @pytest.mark.django_db()
    def test_post_accept(self, client, proposal, url):
        response = client.post(
            url,
            {"action": "accept", "response": "ok"},
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET=proposal.get_hx_target(),
        )
        assert response.status_code == http.HTTPStatus.OK
        proposal.refresh_from_db()
        assert proposal.status_changed_at
        assert proposal.is_accepted()

    @pytest.mark.django_db()
    def test_post_reject(self, client, proposal, url):
        response = client.post(
            url,
            {"action": "reject", "response": "ok"},
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET=proposal.get_hx_target(),
        )
        assert response.status_code == http.HTTPStatus.OK
        proposal.refresh_from_db()
        assert proposal.status_changed_at
        assert proposal.is_rejected()
