"""
To update nflgame.sched.games:

Go to:

cd /Users/conorspicer/anaconda/envs/nflpenv/lib/python3.6/site-packages/nflgame

Then commenting out: _CUR_SCHEDULE = "http://www.nfl.com/liveupdate/scorestrip/postseason/ss.xml"
& un-comment: _CUR_SCHEDULE = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"

py update_sched.py --year 2018
"""

from fixtures.models import Fixture, Team
from accounts.models import User
from datetime import datetime
import nflgame

games = []
game_keys = nflgame.sched.games.keys()
for g in game_keys:
    if g[:4] == '2017' and nflgame.sched.games[g]['season_type'] == "REG" and nflgame.sched.games[g]['month']>2:
        games.append(nflgame.sched.games[g])
# print(len(games))

for g in games:
    if g['away'] == "JAX":
        g['away'] = "JAC"
    if g['home'] == "JAX":
        g['home'] = "JAC"
    t = datetime(
    int(g['year']),
    int(g['month']),
    int(g['day']),
    (int(g['time'].split(':')[0])+12)%24,
    int(g['time'].split(':')[1]),
    )
    new_entry = Fixture(
    name=g['gamekey'],
    away_team = Team.objects.get(short_name=g['away']),
    home_team = Team.objects.get(short_name=g['home']),
    away_score = 0,
    home_score = 0,
    week = g['week'],
    ko_datetime = t
    )
    new_entry.save()
