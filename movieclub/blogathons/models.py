from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
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
        qs = self.filter(published__isnull=False)
        if user.is_authenticated:
            qs = qs | self.for_organizer(user)
        return qs


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

    starts = models.DateField(verbose_name="Start Date")
    ends = models.DateField(verbose_name="End Date")

    description = models.TextField(blank=True)

    published = models.DateTimeField(null=True, blank=True)

    objects = BlogathonQuerySet.as_manager()

    def get_absolute_url(self) -> str:
        """URL of detail page."""
        return reverse(
            "blogathons:blogathon_detail",
            kwargs={"blogathon_id": self.pk, "slug": slugify(self.name)},
        )

    def is_started(self) -> bool:
        """
        If blogathon is open for entries.
        """
        return timezone.now().date() > self.starts

    def is_ended(self) -> bool:
        """
        If blogathon is closed for entries.
        """
        return timezone.now().date() > self.ends

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
            or not self.published
            or user == self.organizer
            or self.is_ended()
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

        if (
            user.is_anonymous
            or not self.published
            or not self.is_started()
            or self.is_ended()
        ):
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

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    status = models.CharField(
        max_length=12,
        default=Status.SUBMITTED,
        choices=Status,
    )

    status_changed_at = models.DateTimeField(null=True, blank=True)

    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blogathon_proposals",
    )

    blogathon = models.ForeignKey(
        Blogathon,
        on_delete=models.CASCADE,
        related_name="proposals",
    )

    proposal = models.TextField()
    response = models.TextField(blank=True)

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["participant", "blogathon"],
                name="%(app_label)s_%(class)s_unique_blogathon_proposal",
                condition=models.Q(status="submitted"),
            )
        ]

    def get_absolute_url(self) -> str:
        """Return detail URL."""
        return reverse("blogathons:proposal_detail", kwargs={"proposal_id": self.pk})

    def is_accepted(self) -> bool:
        """If ACCEPTED status."""
        return self.status == self.Status.ACCEPTED

    def is_rejected(self) -> bool:
        """If REJECTED status."""
        return self.status == self.Status.REJECTED

    def is_submitted(self) -> bool:
        """If SUBMITTED status."""
        return self.status == self.Status.SUBMITTED


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

    blog_title = models.CharField(max_length=300)
    blog_url = models.URLField()
    blog_summary = models.TextField(blank=True)

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["participant", "blogathon"],
                name="%(app_label)s_%(class)s_unique_blogathon_entry",
            )
        ]

    def get_absolute_url(self) -> str:
        """Return detail URL."""
        return reverse("blogathons:entry_detail", kwargs={"entry_id": self.pk})
