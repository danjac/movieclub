from __future__ import annotations

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVectorField
from django.db import models
from django.utils.text import slugify


class Person(models.Model):
    """A crew or cast member."""

    class Gender(models.IntegerChoices):
        UNSPECIFIED = 0, "Unspecified"
        FEMALE = 1, "Female"
        MALE = 2, "Male"

    tmdb_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=120)
    gender = models.PositiveSmallIntegerField(choices=Gender)
    profile_url = models.URLField(blank=True)

    search_vector = SearchVectorField(null=True, editable=False)

    def __str__(self) -> str:
        """Return person's name."""
        return self.name

    @property
    def slug(self) -> str:
        """Return name as slug"""
        return slugify(self.name)


class CastMemberQuerySet(models.QuerySet):
    """CastMember model queryset."""

    def search(self, search_term: str) -> CastMemberQuerySet:
        """Does a full text search"""
        if not search_term:
            return self.none()

        query = SearchQuery(search_term, search_type="websearch")

        return self.annotate(
            person_rank=SearchRank(models.F("person__search_vector"), query=query),
            cast_member_rank=SearchRank(models.F("search_vector"), query=query),
            rank=models.F("person_rank") + models.F("cast_member_rank"),
        ).filter(models.Q(person__search_vector=query) | models.Q(search_vector=query))


class CastMember(models.Model):
    """A cast member"""

    release = models.ForeignKey(
        "releases.Release",
        on_delete=models.CASCADE,
        related_name="cast_members",
    )

    person = models.ForeignKey(
        "credits.Person",
        on_delete=models.CASCADE,
        related_name="cast_members",
    )

    character = models.CharField(max_length=120)
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    search_vector = SearchVectorField(null=True, editable=False)

    objects = CastMemberQuerySet.as_manager()

    def __str__(self) -> str:
        """Returns character name."""
        return self.character


class CrewMemberQuerySet(models.QuerySet):
    """CrewMember model queryset."""

    def search(self, search_term: str) -> CrewMemberQuerySet:
        """Does a full text search"""
        if not search_term:
            return self.none()
        query = SearchQuery(search_term, search_type="websearch")

        return self.annotate(
            person_rank=SearchRank(models.F("person__search_vector"), query=query),
            crew_member_rank=SearchRank(models.F("search_vector"), query=query),
            rank=models.F("person_rank") + models.F("crew_member_rank"),
        ).filter(models.Q(person__search_vector=query) | models.Q(search_vector=query))


class CrewMember(models.Model):
    """A crew member"""

    release = models.ForeignKey(
        "releases.Release",
        on_delete=models.CASCADE,
        related_name="crew_members",
    )

    person = models.ForeignKey(
        "credits.Person",
        on_delete=models.CASCADE,
        related_name="crew_members",
    )
    job = models.CharField(max_length=120)

    search_vector = SearchVectorField(null=True, editable=False)

    objects = CrewMemberQuerySet.as_manager()

    def __str__(self) -> str:
        """Returns job."""
        return self.job
