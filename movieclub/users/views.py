from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST, require_safe

from movieclub.decorators import require_auth, require_DELETE, require_form_methods


@require_safe
def user_details(request: HttpRequest, username: str) -> HttpResponse:
    """Return user details
    * bio
    * links
    * reviews
    * blogathons
    * collections
    """


@require_safe
def user_reviews(request: HttpRequest, username: str) -> HttpResponse:
    """Reviews submitted by the user"""


@require_safe
def user_blogathons(request: HttpRequest, username: str) -> HttpResponse:
    """Blogathons organized or contributed to by this user."""


@require_safe
def user_collections(request: HttpRequest, username: str) -> HttpResponse:
    """Collections belonging to this user."""


@require_form_methods
@require_auth
def edit_user_details(request: HttpRequest) -> HttpResponse:
    """Edit user details"""


@require_POST
@require_auth
def add_user_link(request: HttpRequest) -> HttpResponse:
    """Add a user link"""


@require_form_methods
@require_auth
def edit_user_link(request: HttpRequest, link_id: int) -> HttpResponse:
    """Edit user link"""


@require_DELETE
@require_auth
def remove_user_link(request: HttpRequest, link_id: int) -> HttpResponse:
    """Delete user link"""
