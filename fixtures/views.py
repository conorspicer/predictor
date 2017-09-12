
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.views import generic
from fixtures.models import Fixture, Team
from datetime import datetime, date, timedelta
from scripts.get_week import GetWeek

class ListSpecificWeekFixtures(LoginRequiredMixin, generic.ListView):
    model = Fixture
    def get_context_data(self, **kwargs):
        context = super(ListSpecificWeekFixtures, self).get_context_data(**kwargs)
        q = self.request.GET.get("week")
        context['input'] = q
        return context

    def get_queryset(self):
        # queryset = Fixture.objects.all().order_by('name')
        # queryset = Fixture.objects.all()
        if self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            queryset = Fixture.objects.filter(week=selection).order_by('name')
        else:
            queryset = Fixture.objects.all().order_by('name')
        return queryset
