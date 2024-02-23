from __future__ import annotations

from typing import ClassVar

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


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
