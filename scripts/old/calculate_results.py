from django.contrib.auth.models import User
from fixtures.models import Fixture, Team
from picks.models import Pick
import pandas as pd

def CalculatePoints():
    for p in Pick.objects.all():
        if p.predicted_winner == p.fixture.winner:
            p.winner_pts = 25
        if abs(p.predicted_margin - p.fixture.margin) < 11:
            p.margin_pts = 10 - abs(p.predicted_margin - p.fixture.margin)
        if abs(p.predicted_total_pts - p.fixture.total_pts) < 11:
            p.totalpts_pts = 10 - abs(p.predicted_margin - p.fixture.margin)
        p.save()

def CalculateResults():
    index = list(User.objects.order_by().values_list('username', flat=True).distinct())
    names = list(User.objects.order_by().values_list('username', flat=True).distinct())
    weeks = list(Fixture.objects.order_by().values_list('week', flat=True).distinct())
    weeks.append('TOTAL')
    df = pd.DataFrame(index=index, columns=weeks)

    for index, row in df.iterrows():
        for w in weeks:
            if(w!='TOTAL'):
                week_total = 0
                for p in Pick.objects.filter(fixture__week=w):
                    if(p.fixture.week==w and p.user.username==index):
                        week_total += p.points_scored
                row[w] = week_total

    df['TOTAL'] = df.sum(axis=1)
    return df
