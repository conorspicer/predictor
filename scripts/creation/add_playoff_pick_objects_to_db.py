"""
Run this using:

webapp summary screen > launch console with this venv
cd predictor
python manage.py shell < scripts/creation/add_playoff_pick_objects_to_db.py

"""
import django
django.setup()

from django.contrib.auth.models import User
from fixtures.models import Fixture
from picks.models import Pick
from results.models import UserWeekResult
from scripts.get_week import get_week

current_week = get_week()

for person in User.objects.all():
    for game in Fixture.objects.filter(week=current_week):
        new_entry = Pick(
            fixture=game,
            user=person,
            )
        new_entry.save()

for person in User.objects.all():
    new_entry = UserWeekResult(
        week=current_week,
        user=person,
        )
    new_entry.save()
