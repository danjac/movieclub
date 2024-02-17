from movieclub.credits.models import Person


class TestPerson:
    def test_str(self):
        assert str(Person(name="Keanu Reaves")) == "Keanu Reaves"
