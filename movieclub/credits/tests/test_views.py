import http

import pytest
from django.urls import reverse, reverse_lazy

from movieclub.credits.tests.factories import (
    create_cast_member,
    create_crew_member,
    create_person,
)


@pytest.fixture()
def person():
    return create_person(name="tester")


class TestCastList:
    url = reverse_lazy("credits:cast_list")

    @pytest.mark.django_db()
    def test_get(self, client, person):
        create_cast_member(person=person)
        response = client.get(self.url)

        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_search(self, client, person):
        create_cast_member(person=person)
        response = client.get(self.url, {"query": "tester"})
        assert response.status_code == http.HTTPStatus.OK


class TestCrewList:
    url = reverse_lazy("credits:crew_list")

    @pytest.mark.django_db()
    def test_get(self, client, person):
        create_cast_member(person=person)
        response = client.get(self.url)

        assert response.status_code == http.HTTPStatus.OK

    @pytest.mark.django_db()
    def test_search(self, client, person):
        create_crew_member(person=person)
        response = client.get(self.url, {"query": "tester"})
        assert response.status_code == http.HTTPStatus.OK


class TestCrewDetail:
    @pytest.mark.django_db()
    def test_get(self, client, person):
        create_crew_member(person=person)
        response = client.get(
            reverse(
                "credits:crew_detail",
                kwargs={
                    "person_id": person.pk,
                    "slug": person.slug,
                },
            )
        )
        assert response.status_code == http.HTTPStatus.OK


class TestCastDetail:
    @pytest.mark.django_db()
    def test_get(self, client, person):
        create_cast_member(person=person)
        response = client.get(
            reverse(
                "credits:cast_detail",
                kwargs={
                    "person_id": person.pk,
                    "slug": person.slug,
                },
            )
        )
        assert response.status_code == http.HTTPStatus.OK
