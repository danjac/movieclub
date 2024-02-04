from typing import ClassVar

from django import forms


class BaseReviewForm(forms.ModelForm):
    """Base form."""

    class Meta:
        fields: ClassVar = ["url", "comment"]
