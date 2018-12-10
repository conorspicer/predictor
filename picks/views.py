from django.shortcuts import redirect, render
from .models import Pick
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PickFormSetBase
from scripts.get_week import get_week
from datetime import datetime, timezone, timedelta


# All weeks' picks for logged in user
class ListSpecificWeekPicks(LoginRequiredMixin, generic.ListView):
    model = Pick

    def get_context_data(self, **kwargs):
        context = super(ListSpecificWeekPicks, self).get_context_data(**kwargs)
        q = self.request.GET.get("week")
        context['input'] = q
        context['default'] = get_week()
        return context

    def get_queryset(self):
        queryset = Pick.objects.all()
        if self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            queryset = Pick.objects\
                .filter(user=self.request.user,
                        fixture__week=selection)\
                .order_by('fixture__ko_datetime')
        else:
            queryset = Pick.objects\
                .filter(user=self.request.user)\
                .order_by('fixture__ko_datetime')
        return queryset


# All Users' picks less than 1hr to KO, in play or completed
class ListSubmittedWeekPicks(LoginRequiredMixin, generic.ListView):

    model = Pick
    template_name = 'picks/pick_submitted.html'

    def get_context_data(self, **kwargs):
        context = super(ListSubmittedWeekPicks, self).get_context_data(**kwargs)
        q = self.request.GET.get("week")
        context['input'] = q
        context['current_week'] = get_week()
        return context

    def get_queryset(self):
        # If all selected, don't filter, just order
        if self.request.GET.get("week") == 'All':
            selection = self.request.GET.get("week")
            queryset = Pick.objects.filter(
                fixture__ko_datetime__lt=datetime.now(timezone.utc) - timedelta(hours=3)
            ).order_by('fixture__ko_datetime')

        # if a week is defined, filter on that
        elif self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            queryset = Pick.objects.filter(
                fixture__week=selection,
                fixture__ko_datetime__lt=datetime.now(timezone.utc) - timedelta(hours=3)
            ).order_by('fixture__ko_datetime')

        # otherwise filter to current week
        else:
            queryset = Pick.objects\
                .filter(fixture__week=get_week())\
                .order_by('fixture__ko_datetime')
        return queryset


# All Users' picks
class ListAllWeekPicks(LoginRequiredMixin, generic.ListView):
    model = Pick
    template_name = 'picks/pick_check.html'

    def get_context_data(self, **kwargs):
        context = super(ListAllWeekPicks, self).get_context_data(**kwargs)
        q = self.request.GET.get("week")
        context['input'] = q
        context['current_week'] = get_week()
        return context

    def get_queryset(self):
        # If all selected, don't filter, just order
        if self.request.GET.get("week") == 'All':
            selection = self.request.GET.get("week")
            queryset = Pick.objects\
                .order_by('fixture__ko_datetime')

        # if a week is defined, filter on that
        elif self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            queryset = Pick.objects\
                .filter(fixture__week=selection)\
                .order_by('fixture__ko_datetime')

        # otherwise filter to current week
        else:
            queryset = Pick.objects\
                .filter(fixture__week=get_week())\
                .order_by('fixture__ko_datetime')
        return queryset


class ListSimpleWeekPicks(LoginRequiredMixin, generic.ListView):
    model = Pick
    template_name = 'picks/pick_simple.html'

    def get_queryset(self):
        if self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            queryset = Pick.objects.filter(fixture__week=selection).order_by('fixture__ko_datetime')
        else:
            queryset = Pick.objects.all().order_by('fixture__ko_datetime')
        return queryset


# Picks for logged in user, for current week, with >1hr to KO
@login_required
def UpdatePicks(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        this_week = get_week()
        formset = PickFormSetBase(
            request.POST,
            queryset=Pick.objects.filter(
                fixture__ko_datetime__gt=datetime.now(timezone.utc)-timedelta(hours=5),
                user=request.user,
                fixture__week=this_week
                ).order_by('fixture__ko_datetime')
            )

        print(formset.errors)
        if formset.is_valid():
            for form in formset.forms:
                if action == 'save':
                    form.save()

        redirect('picks:all')

    else:
        formset = PickFormSetBase(
            queryset=Pick.objects.filter(
                fixture__ko_datetime__gt=datetime.now(timezone.utc)-timedelta(hours=5),
                user=request.user,
                fixture__week=get_week()).order_by('fixture__ko_datetime')
        )

    return render(request, 'picks/pick_form.html', {'formset': formset})
