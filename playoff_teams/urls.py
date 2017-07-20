from .views import PlayoffPickList, PlayoffPickUpdate
from django.conf.urls import url

app_name = 'playoff_teams'

urlpatterns = [
    url(r'^$', PlayoffPickList.as_view(), name='all'),
    url(r'^update/$', PlayoffPickUpdate.as_view(), name='update'),
]
