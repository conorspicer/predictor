from django.contrib.auth.models import User
from fixtures.models import Fixture, Team
from picks.models import Pick

for person in User.objects.all():
    for game in Fixture.objects.all():
        new_entry = Pick(
        fixture = game,
        user = person,
        home_pick = 17,
        away_pick = 12,
        )
        new_entry.save()


WEEKS = (
'WK1',
'WK2',
'WK3',
'WK4',
'WK5',
'WK6',
'WK7',
'WK8',
'WK9',
'WK10',
'WK11',
'WK12',
'WK13',
'WK14',
'WK15',
'WK16',
'WK17',
'WILDCARD',
'DIVISIONAL',
'CHAMPIONSHIP',
'SUPERBOWL',
)
