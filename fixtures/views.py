from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.contrib.auth.decorators import login_required
from django.views import generic
from fixtures.models import Fixture, Team
from datetime import datetime, date, timedelta
from scripts.get_week import GetWeek
from .forms import FixtureFormSetBase
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.views import generic

class ListSpecificWeekFixtures(LoginRequiredMixin, generic.ListView):
    model = Fixture
    def get_context_data(self, **kwargs):
        context = super(ListSpecificWeekFixtures, self).get_context_data(**kwargs)
        q = self.request.GET.get("week")
        context['input'] = q
        return context

    def get_queryset(self):
        if self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            queryset = Fixture.objects.filter(week=selection)
            # queryset = Fixture.objects.filter(week=selection).order_by('ko_datetime')
        else:
            queryset = Fixture.objects.all()
            # queryset = Fixture.objects.all().order_by('ko_datetime')
        return queryset

@login_required
def UpdateFixtures(request):
  if request.method == 'POST':
    action = request.POST.get('action')
    formset = FixtureFormSetBase(
        request.POST,
        queryset=Fixture.objects.filter(week=GetWeek()).order_by('ko_datetime')
        )

    print(formset.errors)
    if formset.is_valid():
        for form in formset.forms:
            if action == 'save':
                form.save()

    redirect('fixtures:all')

  else:
      formset = FixtureFormSetBase(
        queryset=Fixture.objects.filter(week=GetWeek()).order_by('ko_datetime')
        )

  return render(request, 'fixtures/fixture_form.html', {'formset': formset})
