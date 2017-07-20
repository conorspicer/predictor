from fixtures.models import Fixture, Team
import nflgame

def UpdateFixtureScores():
    for f in Fixture.objects.all():
        if f.away_team.short_name == "JAC":
            f.away_team.short_name = "JAX"
        if f.home_team.short_name == "JAC":
            f.home_team.short_name = "JAX"
        this_game = nflgame.games(2016, home=f.home_team.short_name, away=f.away_team.short_name)
        f.away_score = this_game[0].score_away
        f.home_score = this_game[0].score_home
        f.save()
