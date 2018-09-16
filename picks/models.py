from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from fixtures.models import Team, Fixture


from django import template
register = template.Library()

from django.contrib.auth import get_user_model
User = get_user_model()


class Pick(models.Model):
    fixture = models.ForeignKey(Fixture, related_name='users_who_picked')
    user = models.ForeignKey(User, related_name='picks')
    home_pick = models.PositiveIntegerField(null=True, blank=True)
    away_pick = models.PositiveIntegerField(null=True, blank=True)
    lock = models.BooleanField(default=False)

    def _get_winner(self):
        if (self.home_pick is not None and self.away_pick is not None):
            if (self.home_pick > self.away_pick):
                return self.fixture.home_team
            if (self.away_pick > self.home_pick):
                return self.fixture.away_team
            else:
                return "Tie"
        else:
            return "Not played"
    predicted_winner = property(_get_winner)

    def _get_margin(self):
        if self.home_pick is not None and self.away_pick is not None:
            return abs(self.home_pick - self.away_pick)
        else:
            return 5000
    predicted_margin = property(_get_margin)

    def _get_totalpts(self):
        if self.home_pick is not None and self.away_pick is not None:
            return self.home_pick + self.away_pick
        else:
            return 5000
    predicted_total_pts = property(_get_totalpts)

    def _winner_pts(self):
        if self.predicted_winner == self.fixture.winner:
            return 25
        else:
            return 0
    winner_pts = property(_winner_pts)

    def _margin_pts(self):
        return  max(10 - abs(self.predicted_margin - self.fixture.margin), 0)
    margin_pts = property(_margin_pts)

    def _totalpts_pts(self):
        return max(10 - abs(self.predicted_total_pts - self.fixture.total_pts), 0)
    totalpts_pts = property(_totalpts_pts)

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
