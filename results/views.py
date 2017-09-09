from django.shortcuts import render
from django.views.generic import ListView
from picks.models import Pick
from .models import UserWeekResult, UserTotalResult
from django.contrib.auth import get_user_model
User = get_user_model()

class ResultsPage(ListView):
    context_object_name = 'results_list'
    template_name = 'results/userweekresult_list.html'

    def get_queryset(self):
        qs = User.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(ResultsPage, self).get_context_data(**kwargs)
        # context['totals'] = UserTotalResult.objects.all().order_by('-total_points_scored')
        context['totals'] = sorted(UserTotalResult.objects.all(), key=lambda x: x.total_points_scored, reverse=True)
        # sorted(UserTotalResult.objects.all(), key=lambda x: x.total_points_scored)
        context['conorspicer'] = UserWeekResult.objects.filter(user__username = 'conorspicer').order_by('week')
        context['torinmehmet'] = UserWeekResult.objects.filter(user__username = 'torinmehmet').order_by('week')
        context['magnusmartinsen'] = UserWeekResult.objects.filter(user__username = 'magnusmartinsen').order_by('week')
        context['lewismead'] = UserWeekResult.objects.filter(user__username = 'lewismead').order_by('week')
        if self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            context['picks'] = Pick.objects.filter(fixture__week=selection, changeable=False).order_by('fixture__name')
        else:
            context['picks'] = Pick.objects.filter(changeable=False).order_by('fixture__name')
        q = self.request.GET.get("week")
        context['input'] = q

        return context
