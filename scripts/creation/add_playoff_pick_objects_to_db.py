"""
Run this using:

webapp summary screen > launch console with this venv
cd predictor
python manage.py shell < scripts/creation/add_playoff_pick_objects_to_db.py

"""
import django

django.setup()

from django.contrib.auth.models import User
from predictor.apps.fixtures.models import Fixture
from predictor.apps.picks.models import Pick
from scripts.get_week import get_week
from datetime import datetime, timedelta, timezone

current_week = get_week()

for person in User.objects.all():
    for game in Fixture.objects.filter(
            week=current_week,
            ko_datetime__gt=datetime.now(timezone.utc) - timedelta(weeks=30)
    ):
        new_entry = Pick(
            fixture=game,
            user=person,

        )
        new_entry.save()

""" 
Equivalent SQL to select Fixture objects:

select *
from fixtures_fixture
where week = 19
  and ko_datetime > DATE_ADD(curdate(), INTERVAL -30 WEEK)
"""
