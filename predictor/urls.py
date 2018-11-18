from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r"^$", views.HomePage.as_view(), name="home"),
    url(r"^test/$", include("picks.urls", namespace="picks")),
    url(r"^thanks/$", views.ThanksPage.as_view(), name="thanks"),
    url(r"^HOF/$", views.HOFPage.as_view(), name="HOF"),
    url(r"^admin/", admin.site.urls),
    url(r"^accounts/", include("accounts.urls", namespace="accounts")),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^fixtures/", include("fixtures.urls", namespace="fixtures")),
    url(r"^picks/", include("picks.urls", namespace="picks")),
    url(r"^results/", include("results.urls", namespace="results")),
    url(r"^playoff_teams/", include("playoff_teams.urls", namespace="playoff_teams")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
