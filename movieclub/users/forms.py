from django import forms

from movieclub.users.models import User


class UserDetailsForm(forms.ModelForm):
    """Form for editing bio etc."""

    class Meta:
        model = User
        fields = ("bio",)
