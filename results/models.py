from django.db import models
from fixtures.models import Team, Fixture
from picks.models import Pick
from playoff_teams.models import PlayoffPick

from django.contrib.auth import get_user_model
User = get_user_model()

class UserWeekResult(models.Model):
    user = models.ForeignKey(User, related_name='player_week')
    week = models.PositiveIntegerField(null=True, blank=True)

    def _user_points(self):
        counter = 0
        for p in Pick.objects.filter(user=self.user, fixture__week=self.week):
            counter += p.points_scored

        # if(self.week<22):
        #     counter = 0
        #     for p in Pick.objects.filter(user=self.user, fixture__week=self.week):
        #         counter += p.points_scored
        # else:
        #     counter = 0
        #     for pp in PlayoffPick.objects.filter(user=self.user):
        #     for pp in PlayoffPick.objects.filter(user="conorspicer"):
        #         for team in [
        #             pp.afc_east,
        #             pp.afc_north,
        #             pp.afc_south,
        #             pp.afc_west,
        #             pp.nfc_east,
        #             pp.nfc_north,
        #             pp.nfc_south,
        #             pp.nfc_west,
        #             pp.afc_wild1,
        #             pp.afc_wild2,
        #             pp.nfc_wild1,
        #             pp.nfc_wild2 ]:
        #             if team.playoff:
        #                 counter += 50
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
