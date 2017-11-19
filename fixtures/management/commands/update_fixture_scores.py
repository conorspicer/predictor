#! /usr/bin/env python3
# from scripts.update_fixture_scores import UpdateFixtureScores

import nflgame
from scripts.get_week import GetWeek
from fixtures.models import Fixture
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def UpdateFixtureScores():
        for f in Fixture.objects.filter(week__lte=GetWeek()):
            if f.away_team.short_name == "JAC":
                f.away_team.short_name = "JAX"
            if f.home_team.short_name == "JAC":
                f.home_team.short_name = "JAX"
            this_game = nflgame.games(2017, home=f.home_team.short_name, away=f.away_team.short_name)
            if this_game != []:
                f.away_score = this_game[0].score_away
                f.home_score = this_game[0].score_home
                f.save()
# UpdateFixtureScores()
