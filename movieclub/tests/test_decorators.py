import http

import pytest
from django.http import HttpResponse
from django.urls import reverse
from django_htmx.middleware import HtmxDetails

from movieclub.decorators import require_auth


class TestRequireAuth:
    @pytest.fixture()
    def view(self):
        return require_auth(lambda req: HttpResponse())

    def test_anonymous_default(self, rf, settings, anonymous_user, view):
        settings.LOGIN_REDIRECT_URL = "/"
        req = rf.get("/new/")
        req.user = anonymous_user
        req.htmx = False
        assert view(req).url == f"{reverse('account_login')}?next=/new/"

    def test_anonymous_htmx(self, rf, settings, anonymous_user, view):
        settings.LOGIN_REDIRECT_URL = "/"
        req = rf.post("/new/", HTTP_HX_REQUEST="true")
        req.user = anonymous_user
        req.htmx = HtmxDetails(req)
        resp = view(req)
        assert resp.headers["HX-Redirect"] == f"{reverse('account_login')}?next=/"

    def test_anonymous_plain_ajax(self, rf, anonymous_user, view):
        req = rf.get("/", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        req.user = anonymous_user
        req.htmx = False
        resp = view(req)
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

    @pytest.mark.django_db()
    def test_authenticated(self, rf, user, view):
        req = rf.get("/")
        req.user = user
        resp = view(req)
        assert resp.status_code == http.HTTPStatus.OK
