import http

import pytest
from django.urls import reverse, reverse_lazy

from movieclub.credits.tests.factories import create_person
from movieclub.movies.tests.factories import create_cast_member, create_crew_member


@pytest.fixture()
def person():
    return create_person()


class TestCastMembers:
    url = reverse_lazy("credits:cast_members")

    @pytest.mark.django_db()
    def test_get(self, client, person):
        create_crew_member(person=person)
        response = client.get(self.url)

        assert response.status_code == http.HTTPStatus.OK


class TestCrewMembers:
    url = reverse_lazy("credits:crew_members")

    @pytest.mark.django_db()
    def test_get(self, client, person):
        create_cast_member(person=person)
        response = client.get(self.url)

        assert response.status_code == http.HTTPStatus.OK


class TestCrewMember:
    @pytest.mark.django_db()
    def test_get(self, client, person):
        create_crew_member(person=person)
        response = client.get(
            reverse(
                "credits:crew_member",
                kwargs={
                    "person_id": person.pk,
                    "slug": person.slug,
                },
            )
        )
        assert response.status_code == http.HTTPStatus.OK


class TestCastMember:
    @pytest.mark.django_db()
    def test_get(self, client, person):
        create_cast_member(person=person)
        response = client.get(
            reverse(
                "credits:cast_member",
                kwargs={
                    "person_id": person.pk,
                    "slug": person.slug,
                },
            )
        )
        assert response.status_code == http.HTTPStatus.OK
