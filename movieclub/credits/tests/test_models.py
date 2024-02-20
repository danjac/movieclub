import pytest

from movieclub.credits.models import CastMember, CrewMember, Person
from movieclub.credits.tests.factories import create_person


class TestPerson:
    @pytest.mark.django_db()
    def test_search_empty(self):
        assert Person.objects.search("").count() == 0

    @pytest.mark.django_db()
    def test_search_on_person_name(self):
        create_person(name="Keanu Reaves")
        assert Person.objects.search("keanu").count() == 1

    def test_str(self):
        assert str(Person(name="Keanu Reaves")) == "Keanu Reaves"


class TestCastMember:
    def test_str(self):
        assert str(CastMember(character="Actor")) == "Actor"


class TestCrewMember:
    def test_str(self):
        assert str(CrewMember(job="Director")) == "Director"
