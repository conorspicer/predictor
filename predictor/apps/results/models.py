from django.db import models
from predictor.apps.picks.models import Pick, Fixture
from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user_model
User = get_user_model()


class UserScores(models.Model):
    pick_id = models.ForeignKey(Pick, on_delete=models.DO_NOTHING, db_column='pick_id')
    ko_datetime = models.DateTimeField(primary_key=True)
    home_pick = models.CharField(max_length=50)
    away_pick = models.CharField(max_length=50)
    locked = models.BooleanField(default=False)
    fixture = models.ForeignKey(Fixture, on_delete=models.DO_NOTHING, db_column='fixture_id')
    away_score = models.PositiveIntegerField(null=True, blank=True)
    home_score = models.PositiveIntegerField(null=True, blank=True)
    week = models.PositiveIntegerField(null=True, blank=True)
    changeable = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user')
    username = models.CharField(max_length=50)
    away_team_name = models.CharField(max_length=50)
    away_team_logo = models.CharField(max_length=150)
    home_team_name = models.CharField(max_length=50)
    home_team_logo = models.CharField(max_length=150)
    user_margin = models.PositiveIntegerField(null=True, blank=True)
    user_total_score = models.PositiveIntegerField(null=True, blank=True)
    user_winner = models.CharField(max_length=50)
    actual_margin = models.PositiveIntegerField(null=True, blank=True)
    actual_total_score = models.PositiveIntegerField(null=True, blank=True)
    actual_winner = models.CharField(max_length=50)
    winner_pts = models.PositiveIntegerField(null=True, blank=True)
    margin_pts = models.PositiveIntegerField(null=True, blank=True)
    total_score_pts = models.PositiveIntegerField(null=True, blank=True)
    user_points = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        # scores by user by game, for current season
        db_table = 'user_scores'


class UserWeekResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user')
    username = models.CharField(max_length=50)
    week = models.PositiveIntegerField(primary_key=True)
    user_points = models.PositiveIntegerField(null=True, blank=True,)

    class Meta:
        managed = False
        # scores by user by week, for current season, with time aware scoring
        db_table = 'user_week_results'


class UserTotalResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    id = models.IntegerField(primary_key=True)

    def _total_points_scored(self):
        counter = 0
        for w in UserWeekResult.objects.filter(user=self.user):
            counter += w.user_points
        return counter
    total_points_scored = property(_total_points_scored)

