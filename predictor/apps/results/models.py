from django.db import models
from predictor.apps.picks.models import Pick
from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user_model
User = get_user_model()


class UserWeekResult(models.Model):
    user = models.ForeignKey(User, related_name='player_week', on_delete=models.CASCADE)
    week = models.PositiveIntegerField(null=True, blank=True)

    def _user_points(self):
        # counter = 0
        # for p in Pick.objects.filter(user=self.user, fixture__week=self.week):
        #     counter += p.points_scored

        if self.week < 22:
            counter = 0
            for p in Pick.objects.filter(
                    user=self.user,
                    fixture__week=self.week,
                    fixture__ko_datetime__gt=datetime.now(timezone.utc) - timedelta(weeks=52),
                    fixture__changeable=1):
                counter += p.points_scored

        # Add manual adjustment for playoff scores
        elif self.user.username == 'conorspicer':
            counter = 0
        elif self.user.username == 'torinmehmet':
            counter = 0
        elif self.user.username == 'magnusmartinsen':
            counter = 0
        elif self.user.username == 'lewismead':
            counter = 0
        else:
            counter = 0
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
    user = models.ForeignKey(User, related_name='player_total', on_delete=models.CASCADE)

    def _total_points_scored(self):
        counter = 0
        for w in UserWeekResult.objects.filter(user=self.user):
            counter += w.user_points
        return counter
    total_points_scored = property(_total_points_scored)

    def __str__(self):
        return self.user.username