from django import forms
from django.forms.models import modelformset_factory
from .models import Fixture
from predictor.formsets import ExistingObjectsFormSet


class FixtureForm(forms.ModelForm):
    class Meta:
        model = Fixture
        fields = ('away_score', 'home_score')

    def clean(self):
        data = super().clean()
        for name in self.Meta.fields:
            if data.get(name) is None:
                self.add_error(name, "Enter a score, including 0 for a shutout.")
        return data


FixtureFormSetBase = modelformset_factory(
    Fixture, extra=0, form=FixtureForm, formset=ExistingObjectsFormSet,
)
