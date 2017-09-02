from results.models import UserWeekResult, UserTotalResult

for result in UserWeekResult.objects.all():
    result.user_points = 0
    result.save()

for total in UserTotalResult.objects.all():
    total.total_points_scored = 0
    total.save()
