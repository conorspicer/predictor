from .views import PlayoffPickList, PlayoffPickUpdate
from django.conf.urls import url

app_name = 'playoff_teams'

urlpatterns = [
    url(r'^$', PlayoffPickList.as_view(), name='all'),
    # url(r'^update/$', PlayoffPickUpdate.as_view(), name='update'),
]

# add this back above final div in playoffpick_list.html to re-enable playoff updates & uncomment above
# <!--<a class="btn btn-success" style="width:200px;" href="{% url 'playoff_teams:update' %}">UPDATE</a>-->
