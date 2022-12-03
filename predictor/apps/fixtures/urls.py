from django.urls import re_path
from . import views

app_name = 'fixtures'

urlpatterns = [
    re_path(r"^$", views.ListSpecificWeekFixtures.as_view(), name="all"),
    re_path(r"^update/$", views.update_fixtures, name="update"),
]
