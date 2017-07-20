from django.db import models
from fixtures.models import Team, Fixture
from picks.models import Pick

from django.contrib.auth import get_user_model
User = get_user_model()

class UserTotalResult(models.Model):
    user = models.ForeignKey(User, related_name='player_total')
    total_points_scored = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class UserWeekResult(models.Model):
    user = models.ForeignKey(User, related_name='player_week')
    week = models.PositiveIntegerField(null=True, blank=True)
    user_points = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return ' '.join([
            self.user.username,
            " - ",
            "Week",
            str(self.week),
        ])
