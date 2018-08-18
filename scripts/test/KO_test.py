from datetime import datetime
from fixtures.models import Fixture, Team
import nflgame

for f in Fixture.objects.all():
    if f.home_team.short_name == "JAC":
        f.home_team.short_name = "JAX"
    if f.away_team.short_name == "JAC":
        f.away_team.short_name = "JAX"
    g = nflgame.games(2016, week=f.week, home=f.home_team.short_name)[0]
    t = datetime(
    int(g.schedule['year']),
    int(g.schedule['month']),
    int(g.schedule['day']),
    (int(g.schedule['time'].split(':')[0])+12)%24,
    int(g.schedule['time'].split(':')[1]),
    )
    if f.home_team.short_name == "JAX":
        f.home_team.short_name = "JAC"
    if f.away_team.short_name == "JAX":
        f.away_team.short_name = "JAC"
    f.ko_datetime = t
    f.save()
