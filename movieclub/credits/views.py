from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from movieclub.credits.models import CrewMember, Person
from movieclub.pagination import render_pagination


@require_safe
def cast_list(request: HttpRequest) -> HttpResponse:
    """List persons."""

    persons = Person.objects.annotate(num_credits=Count("cast_members")).filter(
        num_credits__gt=0
    )

    if request.search:
        persons = persons.search(request.search.value).order_by("-rank")
    else:
        persons = persons.order_by("-num_credits")

    return render_pagination(request, persons, "credits/cast_members.html")


@require_safe
def crew_list(request: HttpRequest) -> HttpResponse:
    """List persons."""

    persons = Person.objects.annotate(num_credits=Count("crew_members")).filter(
        num_credits__gt=0
    )

    if request.search:
        persons = persons.search(request.search.value).order_by("-rank")
    else:
        persons = persons.order_by("-num_credits")

    return render_pagination(request, persons, "credits/crew_members.html")


@require_safe
def cast_detail(request: HttpRequest, person_id: int, slug: str) -> HttpResponse:
    """Render details of a person.
    We probably want 2 views here, for movie cast roles and crew jobs.
    """
    person = get_object_or_404(Person, pk=person_id)

    members = person.cast_members.select_related("release").order_by(
        "-release__release_date"
    )

    is_crew_member = CrewMember.objects.filter(person=person).exists()

    return render_pagination(
        request,
        members,
        "credits/cast_member.html",
        {
            "person": person,
            "is_crew_member": is_crew_member,
        },
    )


@require_safe
def crew_detail(request: HttpRequest, person_id: int, slug: str) -> HttpResponse:
    """Render details of a person.
    We probably want 2 views here, for movie cast roles and crew jobs.
    """
    person = get_object_or_404(Person, pk=person_id)

    members = person.crew_members.select_related("release").order_by(
        "-release__release_date"
    )

    is_cast_member = CrewMember.objects.filter(person=person).exists()

    return render_pagination(
        request,
        members,
        "credits/crew_member.html",
        {
            "person": person,
            "is_cast_member": is_cast_member,
        },
    )
