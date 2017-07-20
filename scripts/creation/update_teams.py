from fixtures.models import Team
import pandas as pd
df = pd.read_csv('files/all_team_names_test.csv')
for index, row in df.iterrows():
    entry = Team.objects.get(short_name = row['short_name'])
    entry.division = row['division']
    entry.save()
