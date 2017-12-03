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

@login_required
def UpdateFixtures(request):
  if request.method == 'POST':
    action = request.POST.get('action')
    formset = FixtureFormSetBase(
        request.POST,
        queryset=Fixture.objects.filter(week=GetWeek())
        )

    print(formset.errors)
    if formset.is_valid():
        for form in formset.forms:
            if action == 'save':
                form.save()

    redirect('fixtures:all')

  else:
      formset = FixtureFormSetBase(
        queryset=Fixture.objects.filter(week=GetWeek())
        )

  return render(request, 'fixtures/fixture_form.html', {'formset': formset})
