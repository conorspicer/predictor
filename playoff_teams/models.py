from django.db import models
from fixtures.models import Team

from django.contrib.auth import get_user_model
User = get_user_model()


class PlayoffPick(models.Model):
    user = models.ForeignKey(User, related_name='playoff_pick')
    afc_north = models.ForeignKey(Team, blank=True, null=True, related_name='afc_north', limit_choices_to={'division': 'AFC_NORTH'},)
    nfc_north = models.ForeignKey(Team, blank=True, null=True, related_name='nfc_north', limit_choices_to={'division': 'NFC_NORTH'},)
    afc_east = models.ForeignKey(Team, blank=True, null=True, related_name='afc_east', limit_choices_to={'division': 'AFC_EAST'},)
    nfc_east = models.ForeignKey(Team, blank=True, null=True, related_name='nfc_east', limit_choices_to={'division': 'NFC_EAST'},)
    afc_west = models.ForeignKey(Team, blank=True, null=True, related_name='afc_west', limit_choices_to={'division': 'AFC_WEST'},)
    nfc_west = models.ForeignKey(Team, blank=True, null=True, related_name='nfc_west', limit_choices_to={'division': 'NFC_WEST'},)
    afc_south = models.ForeignKey(Team, blank=True, null=True, related_name='afc_south', limit_choices_to={'division': 'AFC_SOUTH'},)
    nfc_south = models.ForeignKey(Team, blank=True, null=True, related_name='nfc_south', limit_choices_to={'division': 'NFC_SOUTH'},)
    afc_wild1 = models.ForeignKey(Team, blank=True, null=True, related_name='afc_wild1', limit_choices_to={'conference': 'AFC'},)
    nfc_wild1 = models.ForeignKey(Team, blank=True, null=True, related_name='nfc_wild1', limit_choices_to={'conference': 'NFC'},)
    afc_wild2 = models.ForeignKey(Team, blank=True, null=True, related_name='afc_wild2', limit_choices_to={'conference': 'AFC'},)
    nfc_wild2 = models.ForeignKey(Team, blank=True, null=True, related_name='nfc_wild2', limit_choices_to={'conference': 'NFC'},)
    afc_wild3 = models.ForeignKey(Team, blank=True, null=True, related_name='afc_wild3', limit_choices_to={'conference': 'AFC'}, )
    nfc_wild3 = models.ForeignKey(Team, blank=True, null=True, related_name='nfc_wild3', limit_choices_to={'conference': 'NFC'}, )
    sb_runner_up = models.ForeignKey(Team, blank=True, null=True, related_name='sb_runner_up')
    sb_winner = models.ForeignKey(Team, blank=True, null=True, related_name='sb_winner')

    def __str__(self):
        return ' '.join([
            self.user.username,
            "'s playoff picks",
        ])
