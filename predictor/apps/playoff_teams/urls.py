from .views import PlayoffPickList, PlayoffPickUpdate, PlayoffPickListAll
from django.urls import re_path

app_name = 'playoff_teams'

urlpatterns = [
    re_path(r'^$', PlayoffPickList.as_view(), name='all'),               # individual picks
    re_path(r'^public/$', PlayoffPickListAll.as_view(), name='public'),  # everyone's picks
    re_path(r'^update/$', PlayoffPickUpdate.as_view(), name='update'),
]

# add this back above final div in playoffpick_list.html to re-enable playoff updates & uncomment above
