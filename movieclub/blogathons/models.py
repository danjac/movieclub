from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.conf import settings
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

if TYPE_CHECKING:  # pragma: no cover
    from django.contrib.auth.models import AnonymousUser

    from movieclub.users.models import User


class Blogathon(TimeStampedModel):
    """Blogathon model.

    1. Organizer publishes a new Blogathon.
    2. The Blogathon appears in the "New" tab.
    3. Until the Blogathon starts, participants can submit a proposal.
    4. If proposal is accepted, they can submit an article until the closing date.

    Users can submit one proposal at a time (although can re-submit any number of times).

    Users are allowed one entry each.

    Organizer can also participate.
    """

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

    submitted = models.DateTimeField(null=True, blank=True)

    def can_submit_proposal(self, user: User | AnonymousUser) -> bool:
        """If user is able to submit a proposal."""
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
        """If user is able to submit an entry."""
        if user.is_anonymous or not self.submitted or timezone.now() > self.end_date:
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
