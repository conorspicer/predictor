from datetime import datetime, timezone, timedelta
from django.views.generic import ListView
from predictor.apps.picks.models import Pick
from .models import UserWeekResult, UserTotalResult, UserScores
from scripts.get_week import get_week
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

        # If all selected, don't filter, just order
        if self.request.GET.get("week") == 'All':
            context['valid_picks'] = UserScores.objects \
                .filter(
                ko_datetime__lt=datetime.now(timezone.utc) - timedelta(hours=4),
                changeable=1
            ) \
                .order_by('fixture__ko_datetime')

        # if a week is defined, filter on that
        elif self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            context['valid_picks'] = UserScores.objects \
                .filter(week=selection,
                        changeable=1,
                        ko_datetime__lt=datetime.now(timezone.utc) - timedelta(hours=4)) \
                .order_by('fixture__ko_datetime')

        # otherwise filter to current week
        else:

            context['valid_picks'] = UserScores.objects \
                .filter(week=get_week(),
                        changeable=1,
                        ko_datetime__lt=datetime.now(timezone.utc) - timedelta(hours=4)) \
                .order_by('fixture__ko_datetime')

        q = self.request.GET.get("week")
        context['input'] = q

        return context
