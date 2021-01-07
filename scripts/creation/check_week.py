"""
Run this using:

webapp summary screen > launch console with this venv
cd predictor
python manage.py shell < scripts/creation/check_week.py

"""
import django
django.setup()

from fixtures.models import Fixture
from scripts.get_week import get_week

current_week = get_week()

print('Current week is {week}, number of games this week {games}'.format(
    week=current_week,
    games=Fixture.objects.filter(week=current_week)))

