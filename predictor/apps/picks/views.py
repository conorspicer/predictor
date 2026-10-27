from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import generic

from predictor.weeks import selected_week
from scripts.get_week import get_week
from .forms import PickFormSetBase
from .models import Pick


def pick_deadline_cutoff():
    # Public visibility and editing share the same one-hour-before-kickoff boundary.
    return timezone.now() + timedelta(hours=1)


class WeekPicksMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['input'] = selected_week(self.request)
        return context

    def filter_week(self, queryset):
        week = selected_week(self.request)
        if week != 'All':
            queryset = queryset.filter(fixture__week=week)
        return queryset.select_related('user', 'fixture__away_team',
                                       'fixture__home_team').order_by(
                                           'fixture__ko_datetime', 'fixture_id', 'user_id')


class ListSpecificWeekPicks(LoginRequiredMixin, WeekPicksMixin, generic.ListView):
    model = Pick

    def get_queryset(self):
        return self.filter_week(Pick.objects.filter(
            user=self.request.user, fixture__changeable=True,
        ))


class ListSubmittedWeekPicks(LoginRequiredMixin, WeekPicksMixin, generic.ListView):
    model = Pick
    template_name = 'picks/pick_submitted.html'

    def get_queryset(self):
        return self.filter_week(Pick.objects.filter(
            fixture__changeable=True,
            fixture__ko_datetime__lte=pick_deadline_cutoff(),
        ))


class ListAllWeekPicks(ListSubmittedWeekPicks):
    template_name = 'picks/pick_check.html'


class ListSimpleWeekPicks(ListSubmittedWeekPicks):
    template_name = 'picks/pick_simple.html'


@login_required
def update_picks(request):
    def editable_picks():
        return Pick.objects.filter(
            fixture__changeable=True,
            fixture__ko_datetime__gt=pick_deadline_cutoff(),
            user=request.user,
            fixture__week=get_week(),
        ).select_related('fixture__away_team', 'fixture__home_team').order_by(
            'fixture__ko_datetime', 'pk')

    if request.method == 'POST':
        with transaction.atomic():
            formset = PickFormSetBase(request.POST,
                                     queryset=editable_picks().select_for_update())
            if formset.is_valid() and request.POST.get('action') == 'save':
                formset.save()
                return redirect('picks:all')
    else:
        formset = PickFormSetBase(queryset=editable_picks())
    return render(request, 'picks/pick_form.html', {'formset': formset})
