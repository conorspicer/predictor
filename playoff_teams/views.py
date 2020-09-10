from django.views import generic
from .models import PlayoffPick
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class PlayoffPickList(LoginRequiredMixin, generic.ListView):
    model = PlayoffPick

    def get_queryset(self):
        return PlayoffPick.objects.filter(user=self.request.user)


class PlayoffPickListAll(LoginRequiredMixin, generic.ListView):
    model = PlayoffPick
    template_name = 'playoff_teams/templates/playoff_teams/playoffpick_list.html'

    def get_queryset(self):
        return PlayoffPick.objects.all()


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
        'afc_wild3',
        'nfc_wild3',
        'sb_runner_up',
        'sb_winner'
        )
    # template_name = 'playoffpick_update.html'
    success_url = reverse_lazy('playoff_teams:all')

    def get_object(self):
        return PlayoffPick.objects.get(user=self.request.user)

