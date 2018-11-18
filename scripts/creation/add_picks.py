"""
Run this using:

webapp summary screen > launch console with this venv
cd predictor
python manage.py shell

"""

from django.contrib.auth.models import User
from fixtures.models import Fixture
from picks.models import Pick

for person in User.objects.all():
    for game in Fixture.objects.all():
        new_entry = Pick(fixture=game, user=person)
        new_entry.save()

counter = 0
for person in User.objects.all():
    counter += 1
print(counter)
