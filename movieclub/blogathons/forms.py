import datetime
from typing import ClassVar

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from movieclub.blogathons.models import Blogathon, Entry, Proposal


class CalendarInput(forms.DateInput):
    """Date input using HTML5 date type."""

    input_type = "date"


class BlogathonForm(forms.ModelForm):
    """Blogathon model form."""

    def clean_starts(self) -> datetime.date:
        """Check blogathon starts > today."""
        value = self.cleaned_data["starts"]
        if not self.instance.starts and timezone.now().date() > value:
            raise ValidationError("Blogathon must start at a future date.")
        return value

    def clean(self) -> dict:
        """Check dates."""
        data = super().clean()
        starts = data.get("starts")
        ends = data.get("ends")
        if starts and ends and starts > ends:
            self.add_error("ends", "Blogathon must end after it starts")
        return data

    class Meta:
        model = Blogathon
        fields: ClassVar = [
            "starts",
            "ends",
            "name",
            "description",
        ]
        widgets: ClassVar = {
            "starts": CalendarInput,
            "ends": CalendarInput,
        }


class ProposalForm(forms.ModelForm):
    """Proposal model form."""

    class Meta:
        model = Proposal
        fields: ClassVar = [
            "proposal",
        ]


class ProposalResponseForm(forms.ModelForm):
    """Proposal model form."""

    class Meta:
        model = Proposal
        fields: ClassVar = [
            "proposal",
            "status",
        ]


class EntryForm(forms.ModelForm):
    """Entry model form."""

    class Meta:
        model = Entry
        fields: ClassVar = [
            "blog_title",
            "blog_url",
            "blog_summary",
        ]
