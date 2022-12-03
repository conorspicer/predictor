from django.urls import re_path
from . import views

app_name = 'results'

urlpatterns = [
    re_path(r"^$", views.ResultsPage.as_view(), name="all"),
]
