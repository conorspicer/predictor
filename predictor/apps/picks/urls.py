from django.urls import re_path

from . import views

app_name = 'picks'

urlpatterns = [
    re_path(r"^$", views.ListSpecificWeekPicks.as_view(), name="all"),
    re_path(r'^update/$', views.update_picks, name='update'),
    re_path(r'^public/$', views.ListSubmittedWeekPicks.as_view(), name='public'),
    re_path(r'^check/$', views.ListAllWeekPicks.as_view(), name='check'),
    re_path(r'^simple/$', views.ListSimpleWeekPicks.as_view(), name='check'),
]
