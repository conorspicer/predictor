from fixtures.models import Team
import pandas as pd
df = pd.read_csv('files/all_team_names.csv')
for index, row in df.iterrows():
    new_entry = Team(
    short_name = row['short_name'],
    city_name = row['city_name'],
    team_name = row['team_name'],
    full_name = row['full_name'],
    )
    new_entry.save()


for index, row in df.iterrows():
    print(row['short_name'])
