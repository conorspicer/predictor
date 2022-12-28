"""
Run this using:

webapp summary screen > launch console with this venv
cd predictor
python manage.py shell < scripts/creation/add_picks.py

"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "predictor.settings")
django.setup()

from django.contrib.auth.models import User
from predictor.apps.fixtures.models import Fixture
from predictor.apps.picks.models import Pick


# Initial setup for season
for person in User.objects.all():
    # if person.username == 'lukeconboy':
    for game in Fixture.objects.filter(changeable=1):
        new_entry = Pick(fixture=game, user=person)
        new_entry.save()

# Add picks for playoff weeks:
# from scripts.get_week import get_week
# this_week = get_week()
# for person in User.objects.all():
#     for game in Fixture.objects.filer(week=this_week):
#         new_entry = Pick(fixture=game, user=person)
#         new_entry.save()
