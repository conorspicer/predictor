from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from fixtures.models import Team, Fixture

from django import template
register = template.Library()

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Pick(models.Model):
    fixture = models.ForeignKey(Fixture, related_name='users_who_picked')
    user = models.ForeignKey(User, related_name='picks')
    home_pick = models.PositiveIntegerField(null=True, blank=True)
    away_pick = models.PositiveIntegerField(null=True, blank=True)

    def _get_winner(self):
        if (self.home_pick > self.away_pick):
            return self.fixture.home_team
        if (self.away_pick > self.home_pick):
            return self.fixture.away_team
        else:
            return "Tie"
    predicted_winner = property(_get_winner)

    def _get_margin(self):
        return abs(self.home_pick - self.away_pick)
    predicted_margin = property(_get_margin)

    def _get_totalpts(self):
       return self.home_pick + self.away_pick
    predicted_total_pts = property(_get_totalpts)

    # potentially use this to restrict which can be altered
    # eg if ko > datetime.now(): changeable = true
    changeable = models.BooleanField(default=True)

    winner_pts = models.IntegerField(default = 0)
    margin_pts = models.IntegerField(default = 0)
    totalpts_pts = models.IntegerField(default = 0)

    def _get_total_score(self):
        return (self.winner_pts + self.margin_pts + self.totalpts_pts)
    points_scored = property(_get_total_score)

    def __str__(self):
        return ' '.join([
            self.user.username,
            " - ",
            "Week",
            str(self.fixture.week),
            " - ",
            self.fixture.away_team.team_name,
            " @ ",
            self.fixture.home_team.team_name,
        ])
