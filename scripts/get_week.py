from datetime import datetime, time, timedelta, timezone as datetime_timezone

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone


def _as_utc(value):
    if timezone.is_naive(value):
        return value.replace(tzinfo=datetime_timezone.utc)
    return value.astimezone(datetime_timezone.utc)


def get_week(check_date=None, init_date=None):
    """Count weeks from Wednesday 05:00 UTC after the active season's week 1."""
    check_date = _as_utc(check_date if check_date is not None else timezone.now())
    if init_date is None:
        configured = getattr(settings, 'SEASON_WEEK_ONE_END', '')
        if configured:
            try:
                init_date = datetime.fromisoformat(configured)
            except ValueError as exc:
                raise ImproperlyConfigured(
                    'SEASON_WEEK_ONE_END must be an ISO 8601 datetime.'
                ) from exc
        else:
            from predictor.apps.fixtures.models import Fixture

            kickoff = (Fixture.objects.filter(changeable=True, week=1,
                                              ko_datetime__isnull=False)
                       .order_by('ko_datetime')
                       .values_list('ko_datetime', flat=True).first())
            if kickoff is None:
                return 1
            kickoff = _as_utc(kickoff)
            day = kickoff.date() + timedelta(days=(2 - kickoff.weekday()) % 7)
            init_date = datetime.combine(day, time(5), tzinfo=datetime_timezone.utc)
            if init_date <= kickoff:
                init_date += timedelta(weeks=1)
    elapsed = check_date - _as_utc(init_date)
    return max(1, min(22, elapsed.days // 7 + 2))
