import pytest
from django.template.context import RequestContext

from movieclub.middleware import Pagination
from movieclub.templatetags import cover_image, pagination_url


class TestPaginationUrl:
    def test_url(self, rf):
        request = rf.get("/")
        request.pagination = Pagination(request)
        assert (
            pagination_url(RequestContext(request=request), page_number=3) == "/?page=3"
        )


class TestCoverImage:
    def test_is_cover_url(self):
        dct = cover_image("https://example.com/test.jpg", 100, 150, "test img")
        assert "test.jpg" in dct["cover_url"]
        assert dct["placeholder"] == "https://placehold.co/100x150"

    def test_is_not_cover_url(self):
        dct = cover_image("", 100, 150, "test img")
        assert dct["cover_url"] == ""
        assert dct["placeholder"] == "https://placehold.co/100x150"

    def test_invalid_cover_image_size(self):
        with pytest.raises(AssertionError, match=r"invalid cover image size: 120x600"):
            cover_image("https://example.com/test.jpg", 120, 600, "test img")
