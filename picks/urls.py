from django.conf.urls import url

from . import views

app_name = 'picks'

urlpatterns = [
    url(r"^$", views.ListSpecificWeekPicks.as_view(), name="all"),
    url(r'^update/$', views.UpdatePicks, name='update'),
    url(r'^public/$', views.ListSubmittedWeekPicks.as_view(), name='public'),
    url(r'^check/$', views.ListAllWeekPicks.as_view(), name='check'),
]
