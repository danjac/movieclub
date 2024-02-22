from movieclub.collections.models import Collection


class TestCollection:
    def test_str(self):
        assert str(Collection(name="test")) == "test"
