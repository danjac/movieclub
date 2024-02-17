import http

import pytest
from django.urls import reverse, reverse_lazy

from movieclub.movies.tests.factories import create_cast_member, create_crew_member
from movieclub.people.tests.factories import create_person


@pytest.fixture()
def person():
    return create_person()


class TestCastMembers:
    url = reverse_lazy("people:cast_members")

    @pytest.mark.django_db()
    def test_get(self, client, person):
        create_crew_member(person=person)
        response = client.get(self.url)

        assert response.status_code == http.HTTPStatus.OK


class TestCrewMembers:
    url = reverse_lazy("people:crew_members")

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
                "people:crew_member",
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
                "people:cast_member",
                kwargs={
                    "person_id": person.pk,
                    "slug": person.slug,
                },
            )
        )
        assert response.status_code == http.HTTPStatus.OK
