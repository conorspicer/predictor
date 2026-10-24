from datetime import timedelta

from django import forms
from django.forms.models import modelformset_factory
from django.utils import timezone
from .models import Pick
from predictor.formsets import ExistingObjectsFormSet


class PickForm(forms.ModelForm):
    class Meta:
        model = Pick
        fields = ('away_pick', 'home_pick', 'lock')

    def clean(self):
        data = super().clean()
        if self.instance.pk:
            kickoff = self.instance.fixture.ko_datetime
            if kickoff is None or kickoff <= timezone.now() + timedelta(hours=1):
                raise forms.ValidationError("This pick has closed. Reload the page to see available games.")
        if (data.get('away_pick') is None) != (data.get('home_pick') is None):
            raise forms.ValidationError("Enter both scores, or leave both scores blank.")
        return data


PickFormSetBase = modelformset_factory(
    Pick, extra=0, form=PickForm, formset=ExistingObjectsFormSet,
)
