from django.urls import re_path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'predictor'

urlpatterns = [
    re_path(r"^$", views.HomePage.as_view(), name="home"),
    re_path(r"^test/$", views.TestPage.as_view(), name="test"),
    re_path(r"^thanks/$", views.ThanksPage.as_view(), name="thanks"),
    re_path(r"^HOF/$", views.HOFPage.as_view(), name="HOF"),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^accounts/", include("predictor.apps.accounts.urls", namespace="accounts")),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    re_path(r"^fixtures/", include("predictor.apps.fixtures.urls", namespace="fixtures")),
    re_path(r"^picks/", include("predictor.apps.picks.urls", namespace="picks")),
    re_path(r"^results/", include("predictor.apps.results.urls", namespace="results")),
    re_path(r"^playoff_teams/", include("predictor.apps.playoff_teams.urls", namespace="playoff_teams")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
