import pandas as pd
from datetime import datetime, timezone, timedelta
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .models import UserWeekResult, UserTotalResult, UserScores
from scripts.get_week import get_week
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

        # Results by Week
        data = pd.DataFrame(UserWeekResult.objects.values()).fillna(0).rename(columns={'week': 'Week'})
        pivot = pd.pivot_table(data, index='username', columns='Week', values='user_points')
        pivot.rename(columns={23: 'Playoffs'}, inplace=True)
        pivot.index.name = None
        context['user_results_table'] = pivot.astype(int).to_html().replace(
            'border="1" class="dataframe"', 'style="font-size:20px" class="table"')

        # If all selected, don't filter, just order
        if self.request.GET.get("week") == 'All':
            scores = UserScores.objects\
                .filter(
                    ko_datetime__lt=datetime.now(timezone.utc) - timedelta(hours=4),
                    changeable=1
                )\
                .order_by('fixture__ko_datetime')

        # if a week is defined, filter on that
        elif self.request.GET.get("week"):
            selection = self.request.GET.get("week")
            scores = UserScores.objects\
                .filter(week=selection,
                        changeable=1,
                        ko_datetime__lt=datetime.now(timezone.utc) - timedelta(hours=4))\
                .order_by('fixture__ko_datetime')

        # otherwise filter to current week
        else:
            scores = UserScores.objects\
                .filter(week=get_week(),
                        changeable=1,
                        ko_datetime__lt=datetime.now(timezone.utc) - timedelta(hours=4))\
                .order_by('fixture__ko_datetime')

        scores_df = pd.DataFrame(scores.values())
        if not scores_df.empty:
            tmp = scores_df[[
                'fixture_id',
                'week',
                'away_score',
                'home_score',
                'away_team_logo',
                'home_team_logo',
                'winner_pts',
                'margin_pts',
                'total_score_pts',
            ]].drop_duplicates(['fixture_id'])

            for u in scores_df['username'].unique():
                udf = scores_df[scores_df['username'] == u][[
                    'fixture_id',
                    'user_id',
                    'winner_pts',
                    'margin_pts',
                    'total_score_pts',
                ]]
                tmp = tmp.merge(udf, how='left', on=['fixture_id'], suffixes=['', '_' + u])

            tmp['Matchup'] = '<img src="/static/' + \
                             tmp['away_team_logo'] + \
                             '" style="width:40px;height:40px;"> @ <img src="/static/' + \
                             tmp['home_team_logo'] + \
                             '" style="width:40px;height:40px;">'

            tmp['Score'] = tmp['away_score'].astype(str) + ' - ' + tmp['home_score'].astype(str)

            for u in scores_df['username'].unique():
                tmp[u] = tmp['winner_pts_' + u].astype(str) + '-' + \
                         tmp['margin_pts_' + u].astype(str) + '-' + \
                         tmp['total_score_pts_' + u].astype(str)

            tmp.rename(columns={'week': 'Week'}, inplace=True)
            columns_to_display = ['Week', 'Matchup', 'Score'] + list(scores_df['username'].unique())

            context['valid_picks'] = tmp[columns_to_display].to_html(index=False).replace(
                'border="1" class="dataframe"',
                'style="font-size:20px" class="table"'
            ).replace(r'&lt;img', '<img').replace(r'&gt;', '>')
        else:
            context['valid_picks'] = ''

        q = self.request.GET.get("week")
        context['input'] = q

        return context
