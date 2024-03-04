from django import forms

from movieclub.users.models import Link, User


class UserDetailsForm(forms.ModelForm):
    """Form for editing bio etc."""

    class Meta:
        model = User
        fields = ("bio",)


class LinkForm(forms.ModelForm):
    """Form for adding or editing links"""

    class Meta:
        model = Link
        fields = ("title", "url")
