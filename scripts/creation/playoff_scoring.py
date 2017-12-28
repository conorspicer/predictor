from results.models import UserWeekResult
from django.contrib.auth.models import User
from fixtures.models import Fixture
from picks.models import Pick

for person in User.objects.all():
    new_entry = UserWeekResult(
    week = 18,
    user = person,
    )
    new_entry.save()

# for game in Fixture.objects.filter(week=18):
