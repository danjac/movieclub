from django.db.models import Count, F, OuterRef
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from movieclub.credits.models import Person
from movieclub.movies.models import CastMember as MovieCastMember
from movieclub.movies.models import CrewMember as MovieCrewMember
from movieclub.pagination import render_pagination
from movieclub.tv_shows.models import CastMember as TVShowCastMember
from movieclub.tv_shows.models import CrewMember as TVShowCrewMember


@require_safe
def cast_members(request: HttpRequest) -> HttpResponse:
    """List persons."""

    persons = Person.objects.annotate(
        num_movie_roles=Count(MovieCastMember.objects.filter(person=OuterRef("pk"))),
        num_tv_show_roles=Count(TVShowCastMember.objects.filter(person=OuterRef("pk"))),
        num_roles=F("num_tv_show_roles") + F("num_movie_roles"),
    ).filter(num_roles__gt=0)

    return render_pagination(request, persons, "credits/cast_members.html")


@require_safe
def crew_members(request: HttpRequest) -> HttpResponse:
    """List persons."""

    persons = Person.objects.annotate(
        num_movie_roles=Count(MovieCrewMember.objects.filter(person=OuterRef("pk"))),
        num_tv_show_roles=Count(TVShowCrewMember.objects.filter(person=OuterRef("pk"))),
        num_roles=F("num_tv_show_roles") + F("num_movie_roles"),
    ).filter(num_roles__gt=0)

    return render_pagination(request, persons, "credits/crew_members.html")


@require_safe
def cast_member(request: HttpRequest, person_id: int, slug: str) -> HttpResponse:
    """Render details of a person.
    We probably want 2 views here, for movie cast roles and crew jobs.
    """
    person = get_object_or_404(Person, pk=person_id)

    members = (
        MovieCastMember.objects.filter(person=person)
        .order_by("-movie__release_date")
        .union(
            TVShowCastMember.objects.filter(person=person).order_by(
                "-tv_show__release_date"
            )
        )
    )

    return render_pagination(
        request,
        members,
        "credits/cast_member.html",
        {
            "person": person,
            "is_crew_member": False,
        },
    )


@require_safe
def crew_member(request: HttpRequest, person_id: int, slug: str) -> HttpResponse:
    """Render details of a person.
    We probably want 2 views here, for movie cast roles and crew jobs.
    """
    person = get_object_or_404(Person, pk=person_id)

    members = MovieCrewMember.objects.filter(person=person).union(
        TVShowCrewMember.objects.filter(person=person)
    )

    return render_pagination(
        request,
        members,
        "credits/crew_member.html",
        {
            "person": person,
            "is_cast_member": False,
        },
    )
