from django import forms
from django.forms.models import modelformset_factory
from .models import Pick


class PickForm(forms.ModelForm):
    class Meta:
        model = Pick
        exclude = ()


PickFormSetBase = modelformset_factory(Pick, extra=0, form=PickForm,
                                       fields=('fixture', 'away_pick', 'home_pick', 'lock'))
