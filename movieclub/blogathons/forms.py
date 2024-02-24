from typing import ClassVar

from django import forms

from movieclub.blogathons.models import Blogathon, Entry, Proposal


class BlogathonForm(forms.ModelForm):
    """Blogathon model form."""

    class Meta:
        model = Blogathon
        fields: ClassVar = [
            "start_date",
            "end_date",
            "name",
            "description",
        ]


class ProposalForm(forms.ModelForm):
    """Proposal model form."""

    class Meta:
        model = Proposal
        fields: ClassVar = [
            "proposal",
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
