from django.shortcuts import redirect, render
from django.template import RequestContext
from .models import Pick
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PickFormSetBase
from fixtures.models import Fixture
from scripts.get_week import GetWeek
from results.models import UserWeekResult
from datetime import datetime, timezone, timedelta

# All weeks' picks for logged in user
class ListSpecificWeekPicks(LoginRequiredMixin, generic.ListView):
    model = Pick
    def get_context_data(self, **kwargs):
        context = super(ListSpecificWeekPicks, self).get_context_data(**kwargs)
        q = self.request.GET.get("week")
        context['input'] = q
        context['default'] = GetWeek()
        return context

    def get_queryset(self):
        queryset = Pick.objects.all()
        if self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            queryset = Pick.objects.filter(user=self.request.user, fixture__week=selection)
        else:
            queryset = Pick.objects.filter(user=self.request.user)
        return queryset

# All Users' picks less than 1hr to KO, in play or completed
class ListSubmittedWeekPicks(LoginRequiredMixin, generic.ListView):
    model = Pick
    template_name = 'picks/pick_submitted.html'
    def get_context_data(self, **kwargs):
        context = super(ListSubmittedWeekPicks, self).get_context_data(**kwargs)
        q = self.request.GET.get("week")
        context['input'] = q
        return context


    def get_queryset(self):
        # queryset = Pick.objects.all()
        if self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            queryset = Pick.objects.filter(fixture__week=selection, fixture__ko_datetime__lt=datetime.now(timezone.utc) - timedelta(hours=3)).order_by('fixture__name')
        else:
            queryset = Pick.objects.filter(fixture__ko_datetime__lt=datetime.now(timezone.utc) - timedelta(hours=3)).order_by('fixture__name')
        return queryset

# Picks for logged in user, for current week, with >1hr to KO
@login_required
def UpdatePicks(request):
  if request.method == 'POST':
    action = request.POST.get('action')
    this_week = GetWeek()
    formset = PickFormSetBase(
        request.POST,
        queryset=Pick.objects.filter(fixture__ko_datetime__gt=datetime.now(timezone.utc) - timedelta(hours=3), user=request.user, fixture__week=this_week)
        )

    print(formset.errors)
    if formset.is_valid():
        for form in formset.forms:
            if action == 'save':
                form.save()

    redirect('picks:all')

  else:
      this_week = GetWeek()
      formset = PickFormSetBase(
        queryset=Pick.objects.filter(fixture__ko_datetime__gt=datetime.now(timezone.utc) - timedelta(hours=3), user=request.user, fixture__week=GetWeek() )
        )

  # return render(request, 'picks/pick_form.html', {'formset': formset}, content_type=RequestContext(request))
  return render(request, 'picks/pick_form.html', {'formset': formset})
