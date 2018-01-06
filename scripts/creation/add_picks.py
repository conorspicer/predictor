from django.contrib.auth.models import User
from fixtures.models import Fixture
from picks.models import Pick
from scripts.get_week import GetWeek

for person in User.objects.all():
    for game in Fixture.objects.all():
        new_entry = Pick(
        fixture = game,
        user = person,
        )
        new_entry.save()

# Add picks for playoff weeks:
this_week = GetWeek()
for person in User.objects.all():
    for game in Fixture.objects.filer(week=this_week):
        new_entry = Pick(
        fixture = game,
        user = person,
        )
        new_entry.save()

counter = 0
for person in User.objects.all():
    counter += 1
print(counter)
