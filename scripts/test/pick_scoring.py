from picks.models import Pick
from fixtures.models import Fixture, Team

for p in Pick.objects.all():
    if p.predicted_winner == p.fixture.winner:
        p.winner_pts = 25
    p.margin_pts = max(10 - abs(p.predicted_margin - p.fixture.margin), 0)
    p.totalpts_pts = max(10 - abs(p.predicted_total_pts - p.fixture.total_pts), 0)
    p.save()
