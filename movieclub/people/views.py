from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from movieclub.pagination import render_pagination
from movieclub.people.models import Person


@require_safe
def cast_members(request: HttpRequest) -> HttpResponse:
    """List persons."""

    persons = Person.objects.annotate(
        num_movies=Count("movies_as_cast_member"),
    ).filter(num_movies__gt=0)

    return render_pagination(request, persons, "people/cast_members.html")


@require_safe
def crew_members(request: HttpRequest) -> HttpResponse:
    """List persons."""

    persons = Person.objects.annotate(
        num_movies=Count("movies_as_crew_member"),
    ).filter(num_movies__gt=0)

    return render_pagination(request, persons, "people/crew_members.html")


@require_safe
def cast_member(request: HttpRequest, person_id: int, slug: str) -> HttpResponse:
    """Render details of a person.
    We probably want 2 views here, for movie cast roles and crew jobs.
    """
    person = get_object_or_404(Person, pk=person_id)
    is_crew_member = person.movies_as_crew_member.exists()
    return render_pagination(
        request,
        person.movies_as_cast_member.select_related("movie").order_by(
            "-movie__release_date"
        ),
        "people/cast_member.html",
        {
            "person": person,
            "is_crew_member": is_crew_member,
        },
    )


@require_safe
def crew_member(request: HttpRequest, person_id: int, slug: str) -> HttpResponse:
    """Render details of a person.
    We probably want 2 views here, for movie cast roles and crew jobs.
    """
    person = get_object_or_404(Person, pk=person_id)
    is_cast_member = person.movies_as_cast_member.exists()
    return render_pagination(
        request,
        person.movies_as_crew_member.select_related("movie").order_by(
            "-movie__release_date"
        ),
        "people/crew_member.html",
        {
            "person": person,
            "is_cast_member": is_cast_member,
        },
    )
