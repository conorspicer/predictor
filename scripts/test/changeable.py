# for p in Pick.objects.all():
#     if p.changeable == False:
#         p.changeable = True
#         p.save()
# Make picks no longer changeable 1 hour before KO
# Assuming script is run hourly? Or prevent form submissions if too close?
# What if form is left loaded & picks then changed?

from datetime import datetime, timezone, timedelta
from scripts.get_week import get_week
from picks.models import Pick

 - timedelta(hours=3)

w = get_week()
for p in Pick.objects.filter(fixture__week=w):
    if p.fixture.ko_datetime < datetime.now(timezone.utc)  - timedelta(hours=3):
        print(p)


            # p.changeable = False
            # p.save()
