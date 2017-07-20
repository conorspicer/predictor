from fixtures.models import Fixture, Team
from accounts.models import User
import nflgame
games = nflgame.games(2016, kind='REG')
for g in games:
    if g.away == "JAX":
        g.away = "JAC"
    if g.home == "JAX":
        g.home = "JAC"
    t = datetime(
    int(g.schedule['year']),
    int(g.schedule['month']),
    int(g.schedule['day']),
    (int(g.schedule['time'].split(':')[0])+12)%24,
    int(g.schedule['time'].split(':')[1]),
    )
    new_entry = Fixture(
    name=g.gamekey,
    away_team = Team.objects.get(short_name=g.away),
    home_team = Team.objects.get(short_name=g.home),
    away_score=g.score_away,
    home_score=g.score_home,
    week=g.schedule['week'],
    ko_datetime=t
    )
    new_entry.save()
