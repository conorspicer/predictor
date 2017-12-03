from django import forms
from django.forms.models import modelformset_factory
from .models import Fixture

#forms.py
class FixtureForm(forms.ModelForm):
    class Meta:
        model = Fixture
        exclude = ()

FixtureFormSetBase = modelformset_factory(Fixture, extra=0, form=FixtureForm,fields=('away_score', 'home_score'))
