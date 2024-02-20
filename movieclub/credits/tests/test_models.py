import pytest

from movieclub.credits.models import CastMember, CrewMember, Person
from movieclub.credits.tests.factories import (
    create_cast_member,
    create_crew_member,
    create_person,
)


class TestPerson:
    def test_str(self):
        assert str(Person(name="Keanu Reaves")) == "Keanu Reaves"


class TestCastMember:
    @pytest.mark.django_db()
    def test_search_empty(self):
        assert CastMember.objects.search("").count() == 0

    @pytest.mark.django_db()
    def test_search_on_person_name(self):
        create_cast_member(person=create_person(name="Keanu Reaves"))
        assert CastMember.objects.search("keanu").count() == 1

    @pytest.mark.django_db()
    def test_search_on_character(self):
        create_cast_member(person=create_person(name="John Wick"))
        assert CastMember.objects.search("wick").count() == 1

    def test_str(self):
        assert str(CastMember(character="Actor")) == "Actor"


class TestCrewMember:
    @pytest.mark.django_db()
    def test_search_empty(self):
        assert CrewMember.objects.search("").count() == 0

    @pytest.mark.django_db()
    def test_search_on_person_name(self):
        create_crew_member(person=create_person(name="John Williams"))
        assert CrewMember.objects.search("williams").count() == 1

    @pytest.mark.django_db()
    def test_search_on_character(self):
        create_crew_member(job="Composer")
        assert CrewMember.objects.search("composer").count() == 1

    def test_str(self):
        assert str(CrewMember(job="Director")) == "Director"
