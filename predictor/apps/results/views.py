from datetime import timedelta
from django.utils import timezone
from django.views.generic import ListView
from predictor.apps.picks.models import Pick
from .models import UserWeekResult, UserTotalResult, UserScores
from scripts.get_week import get_week
from django.contrib.auth import get_user_model
from predictor.weeks import selected_week
User = get_user_model()


class ResultsPage(ListView):
    context_object_name = 'results_list'
    template_name = 'results/userweekresult_list.html'

    def get_queryset(self):
        qs = User.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        week = selected_week(self.request)
        context = super(ResultsPage, self).get_context_data(**kwargs)

        context['current_week'] = get_week()

        context['totals'] = sorted(UserTotalResult.objects.all(),
                                   key=lambda x: x.total_points_scored, reverse=True)

        context['conorspicer'] = UserWeekResult.objects \
            .filter(user__username='conorspicer') \
            .order_by('week')

        context['torinmehmet'] = UserWeekResult.objects \
            .filter(user__username='torinmehmet') \
            .order_by('week')

        context['magnusmartinsen'] = UserWeekResult.objects \
            .filter(user__username='magnusmartinsen') \
            .order_by('week')

        context['lewismead'] = UserWeekResult.objects \
            .filter(user__username='lewismead') \
            .order_by('week')

        valid_picks = UserScores.objects.filter(
            ko_datetime__lt=timezone.now() - timedelta(hours=4),
            changeable=True,
        )
        if week != 'All':
            valid_picks = valid_picks.filter(week=week)
        context['valid_picks'] = valid_picks.select_related(
            'fixture__away_team', 'fixture__home_team', 'user',
        ).order_by('fixture_id', 'user_id')

        context['input'] = week

        return context
