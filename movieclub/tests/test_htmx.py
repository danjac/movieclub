import pytest

from movieclub.htmx import render_htmx


class TestRenderHtmx:
    @pytest.fixture()
    def mock_render(self, mocker):
        return mocker.patch("movieclub.htmx.render")

    def test_not_htmx(self, rf, mock_render):
        request = rf.get("/")
        request.htmx = False
        render_htmx(request, "index.html", {}, partial="form")
        mock_render.assert_called_with(request, "index.html", {})

    def test_htmx(self, rf, mock_render):
        request = rf.get("/")
        request.htmx = True
        render_htmx(request, "index.html", {}, partial="form")
        mock_render.assert_called_with(request, "index.html#form", {})

    def test_htmx_target_not_match(self, rf, mocker, mock_render):
        request = rf.get("/")
        request.htmx = mocker.Mock()
        request.htmx.target = None
        render_htmx(request, "index.html", {}, partial="form", target="my-form")
        mock_render.assert_called_with(request, "index.html", {})

    def test_htmx_target_match(self, rf, mocker, mock_render):
        request = rf.get("/")
        request.htmx = mocker.Mock()
        request.htmx.target = "my-form"
        render_htmx(request, "index.html", {}, partial="form", target="my-form")
        mock_render.assert_called_with(request, "index.html#form", {})
