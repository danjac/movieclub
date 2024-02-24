from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.conf import settings
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

if TYPE_CHECKING:  # pragma: no cover
    from django.contrib.auth.models import AnonymousUser

    from movieclub.users.models import User


class BlogathonQuerySet(models.QuerySet):
    """Queryset for blogathon."""

    def for_organizer(self, user: User) -> models.QuerySet[Blogathon]:
        """Returns all blogathons for organized by this user."""
        return self.filter(organizer=user) if user.is_authenticated else self.none()

    def available(self, user: User | AnonymousUser) -> models.QuerySet[Blogathon]:
        """Returns all available blogathons"""
        return self.filter(published__isnull=False) | self.for_organizer(user)


class Blogathon(TimeStampedModel):
    """Blogathon model."""

    name = models.CharField(max_length=120)

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blogathons",
    )

    starts = models.DateField()
    ends = models.DateField()

    description = models.TextField(blank=True)

    published = models.DateTimeField(null=True, blank=True)

    objects = BlogathonQuerySet.as_manager()

    def can_submit_proposal(self, user: User | AnonymousUser) -> bool:
        """If user is able to submit a proposal.

        A proposal:

            1) must be submitted by a logged in user;
            2) cannot be the blogathon organizer;
            3) must be submitted before the blogathon start date.

        A participant can only have one SUBMITTED or ACCEPTED proposal per blogathon.
        """
        if (
            user.is_anonymous
            or not self.submitted
            or user == self.organizer
            or timezone.now() > self.start_date
        ):
            return False
        return not self.proposals.filter(
            participant=user,
            status__in=(
                Proposal.Status.ACCEPTED,
                Proposal.Status.SUBMITTED,
            ),
        ).exists()

    def can_submit_entry(self, user: User | AnonymousUser) -> bool:
        """If user is able to submit an entry.

        An entry:
            1) must be submitted by a logged in user;
            2) must be either the organizer OR have had a successful proposal;
            3) must be submitted before the end date of the blogathon.

        A participant can only submit one entry per blogathon.
        """
        if user.is_anonymous or not self.published or timezone.now() > self.end_date:
            return False

        if self.entries.filter(participant=user).exists():
            return False

        if user == self.organizer:
            return True

        return self.proposals.filter(
            participant=user,
            status=Proposal.Status.ACCEPTED,
        ).exists()


class Proposal(TimeStampedModel):
    """Blogathon entry proposal."""

    class State(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    state = models.CharField(
        max_length=12,
        default=State.SUBMITTED,
        choices=State,
    )

    state_changed_at = models.DateTimeField(null=True, blank=True)

    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blogathon_proposals",
    )

    blogathon = models.ForeignKey(
        Blogathon,
        on_delete=models.CASCADE,
        related_name="proposals",
    )

    proposal = models.TextField(blank=True)
    response = models.TextField(blank=True)

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["participant", "blogathon"],
                name="%(app_label)s_%(class)s_unique_blogathon_proposal",
                condition=models.Q(state="submitted"),
            )
        ]


class Entry(TimeStampedModel):
    """Blogathon entry."""

    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blogathon_entries",
    )

    blogathon = models.ForeignKey(
        Blogathon,
        on_delete=models.CASCADE,
        related_name="entries",
    )

    blog_title = models.CharField(max_length=300, blank=True)
    blog_url = models.URLField(blank=True)
    blog_summary = models.TextField(blank=True)

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["participant", "blogathon"],
                name="%(app_label)s_%(class)s_unique_blogathon_entry",
            )
        ]
