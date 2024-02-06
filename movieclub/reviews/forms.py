from typing import ClassVar

from django import forms
from django.core.validators import MaxLengthValidator


class BaseReviewForm(forms.ModelForm):
    """Base form."""

    class Meta:
        fields: ClassVar = ["comment", "url"]
        help_texts: ClassVar = {
            "url": "URL to Blog Page",
            "comment": "Review (max 500 chars)",
        }
        validators: ClassVar = {
            "comment": MaxLengthValidator(500, "Max 500 characters")
        }
