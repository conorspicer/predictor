from fixtures.models import Team
from django.views import generic
from .models import PlayoffPick
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class PlayoffPickList(LoginRequiredMixin, generic.ListView):
    model = PlayoffPick

    def get_queryset(self):
        return PlayoffPick.objects.filter(user=self.request.user)

class PlayoffPickUpdate(LoginRequiredMixin, generic.UpdateView):
    model = PlayoffPick
    fields = (
        'afc_north',
        'nfc_north',
        'afc_east',
        'nfc_east',
        'afc_west',
        'nfc_west',
        'afc_south',
        'nfc_south',
        'afc_wild1',
        'nfc_wild1',
        'afc_wild2',
        'nfc_wild2',
        )
    # template_name = 'playoffpick_update.html'
    success_url = reverse_lazy('playoff_teams:all')

    def get_object(self):
        return PlayoffPick.objects.get(user=self.request.user)
