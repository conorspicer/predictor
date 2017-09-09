from django.db import models
from fixtures.models import Team, Fixture
from picks.models import Pick

from django.contrib.auth import get_user_model
User = get_user_model()

class UserWeekResult(models.Model):
    user = models.ForeignKey(User, related_name='player_week')
    week = models.PositiveIntegerField(null=True, blank=True)

    def _user_points(self):
        counter = 0
        for p in Pick.objects.filter(user=self.user, fixture__week=self.week):
            counter += p.points_scored
        return counter
    user_points = property(_user_points)

    def __str__(self):
        return ' '.join([
            self.user.username,
            " - ",
            "Week",
            str(self.week),
        ])

class UserTotalResult(models.Model):
    user = models.ForeignKey(User, related_name='player_total')

    def _total_points_scored(self):
        counter = 0
        for w in UserWeekResult.objects.filter(user=self.user):
            counter += w.user_points
        return counter
    total_points_scored = property(_total_points_scored)

    def __str__(self):
        return self.user.username
