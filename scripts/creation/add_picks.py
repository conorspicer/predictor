"""
Run this using:

webapp summary screen > launch console with this venv
cd predictor
python manage.py shell < scripts/creation/add_picks.py

"""

from django.contrib.auth.models import User
from fixtures.models import Fixture
from picks.models import Pick
from scripts.get_week import get_week

# Inital setup for season
for person in User.objects.all():
    for game in Fixture.objects.filter(changeable=1):
        new_entry = Pick(fixture=game, user=person)
        new_entry.save()

# Add picks for playoff weeks:
# this_week = get_week()
# for person in User.objects.all():
#     for game in Fixture.objects.filer(week=this_week):
#         new_entry = Pick(fixture=game, user=person)
#         new_entry.save()
