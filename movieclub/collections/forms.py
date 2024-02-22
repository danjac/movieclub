from typing import ClassVar

from django import forms

from movieclub.collections.models import Collection


class CollectionForm(forms.ModelForm):
    """Form for collections."""

    class Meta:
        model = Collection
        fields: ClassVar = ["name"]
