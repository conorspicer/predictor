from django import forms
from django.forms.models import BaseModelFormSet


class ExistingObjectsFormSet(BaseModelFormSet):
    """Only update distinct objects in the server-selected queryset."""

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields[self.model._meta.pk.name].queryset = self.get_queryset()

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        seen = set()
        for form in self.forms:
            obj = form.cleaned_data.get(self.model._meta.pk.name)
            if obj is None or obj.pk != form.instance.pk or obj.pk in seen:
                raise forms.ValidationError(
                    "These entries are no longer available. Reload the page and try again."
                )
            seen.add(obj.pk)
