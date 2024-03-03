import pytest

from movieclub.releases.templatetags.releases import (
    get_latest_releases,
    get_random_release,
)
from movieclub.releases.tests.factories import create_movie
from movieclub.tests.factories import create_batch


@pytest.fixture()
def movies():
    return create_batch(create_movie, 6)


class TestGetLatestReleases:
    @pytest.mark.django_db()
    def test_get_releases(self, movies):
        assert len(get_latest_releases(3)) == 3


class TestGetRandomRelease:
    @pytest.mark.django_db()
    def test_get_release(self, movies):
        assert get_random_release()
