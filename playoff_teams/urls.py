from .views import PlayoffPickList, PlayoffPickUpdate, PlayoffPickListAll
from django.conf.urls import url

app_name = 'playoff_teams'

urlpatterns = [
    url(r'^$', PlayoffPickList.as_view(), name='all'),               # individual picks
    url(r'^public/$', PlayoffPickListAll.as_view(), name='public'),  # everyone's picks
    url(r'^update/$', PlayoffPickUpdate.as_view(), name='update'),
]

# add this back above final div in playoffpick_list.html to re-enable playoff updates & uncomment above
