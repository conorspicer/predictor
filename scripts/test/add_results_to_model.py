from fixtures.models import Fixture
from predictor.apps.picks.models import Pick
from predictor.apps.results import UserWeekResult, UserTotalResult

weeks = list(Fixture.objects.order_by().values_list('week', flat=True).distinct())

# Initial check & creation of new if required:
# for user in User.objects.all():
#     for w in weeks:
#         obj, created = UserWeekResult.objects.get_or_create(
#             week=w,
#             user=user,
#         )
# for user in User.objects.all():
#         obj, created = UserTotalResult.objects.get_or_create(
#             user=user,
#         )

# Add up weekly scores by user:
for result in UserWeekResult.objects.all():
    counter = 0
    for p in Pick.objects.filter(user=result.user, fixture__week=result.week):
        counter += p.points_scored
    result.user_points = counter
    result.save()

# Adding user grand totals over all weeks:
for total in UserTotalResult.objects.all():
    counter = 0
    for w in UserWeekResult.objects.filter(user=total.user):
        counter += w.user_points
    total.total_points_scored = counter
    total.save()
