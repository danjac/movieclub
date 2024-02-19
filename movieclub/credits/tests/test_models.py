from movieclub.credits.models import CastMember, CrewMember, Person


class TestPerson:
    def test_str(self):
        assert str(Person(name="Keanu Reaves")) == "Keanu Reaves"


class TestCastMember:
    def test_str(self):
        assert str(CastMember(character="Actor")) == "Actor"


class TestCrewMember:
    def test_str(self):
        assert str(CrewMember(job="Director")) == "Director"
