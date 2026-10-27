from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.views import generic

from predictor.weeks import selected_week
from scripts.get_week import get_week
from .forms import FixtureFormSetBase
from .models import Fixture


class ListSpecificWeekFixtures(LoginRequiredMixin, generic.ListView):
    model = Fixture

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['input'] = selected_week(self.request, default_current=False)
        return context

    def get_queryset(self):
        queryset = Fixture.objects.filter(changeable=True)
        week = selected_week(self.request, default_current=False)
        if week != 'All':
            queryset = queryset.filter(week=week)
        return queryset.select_related('away_team', 'home_team').order_by('ko_datetime', 'pk')


@login_required
@permission_required('fixtures.change_fixture', raise_exception=True)
def update_fixtures(request):
    queryset = (Fixture.objects.filter(week=get_week(), changeable=True)
                .select_related('away_team', 'home_team').order_by('ko_datetime', 'pk'))
    if request.method == 'POST':
        with transaction.atomic():
            formset = FixtureFormSetBase(request.POST, queryset=queryset.select_for_update())
            if formset.is_valid() and request.POST.get('action') == 'save':
                formset.save()
                return redirect('fixtures:all')
    else:
        formset = FixtureFormSetBase(queryset=queryset)
    return render(request, 'fixtures/fixture_form.html', {'formset': formset})
