from django.conf.urls import url
from . import views

app_name = 'fixtures'

urlpatterns = [
    url(r"^$", views.ListSpecificWeekFixtures.as_view(), name="all"),
    url(r"^update/$", views.UpdateFixtures, name="update"),
]
