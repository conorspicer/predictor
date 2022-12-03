import pandas as pd
from predictor.apps.picks.models import Pick
from fixtures.models import Fixture
from django_pandas.io import read_frame

# Take all picks from DB
qs = Pick.objects.select_related('fixture').select_related('user')
df = read_frame(qs)

# Collect all fixtures and picks info from DB
pd.DataFrame(list(Fixture.objects.all().values())).to_csv('fixtures_output.csv')
pd.DataFrame(list(Pick.objects.all().values())).to_csv('picks_output.csv')

picks = pd.DataFrame(list(Pick.objects.filter(user__username="torinmehmet").values()))
fixtures = pd.DataFrame(list(Fixture.objects.all().values()))
picks.set_index('fixture_id').join(fixtures.set_index('id')).to_csv('mehmet.csv')
