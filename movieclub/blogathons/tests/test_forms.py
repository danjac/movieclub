from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from movieclub.blogathons.forms import BlogathonForm


class TestBlogathonForm:
    def form_data(self, starts, ends):
        return {
            "name": "test",
            "description": "test",
            "starts": starts.strftime(settings.DATE_INPUT_FORMATS[0]),
            "ends": ends.strftime(settings.DATE_INPUT_FORMATS[0]),
        }

    def test_ok(self):
        now = timezone.now()
        starts = now + timedelta(days=1)
        ends = starts + timedelta(days=7)

        form = BlogathonForm(self.form_data(starts, ends))
        assert form.is_valid()

    def test_starts_before_now(self):
        now = timezone.now()
        starts = now - timedelta(days=1)
        ends = starts + timedelta(days=7)

        form = BlogathonForm(self.form_data(starts, ends))
        assert not form.is_valid()

    def test_ends_before_starts(self):
        now = timezone.now()
        starts = now + timedelta(days=1)
        ends = starts - timedelta(days=7)

        form = BlogathonForm(self.form_data(starts, ends))
        assert not form.is_valid()
